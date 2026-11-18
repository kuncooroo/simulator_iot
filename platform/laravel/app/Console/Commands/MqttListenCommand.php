<?php

namespace App\Console\Commands;

use App\Models\Telemetry;
use Illuminate\Console\Command;
use PhpMqtt\Client\ConnectionSettings;
use PhpMqtt\Client\MqttClient;

/**
 * Subscriber MQTT di dalam Laravel.
 *
 * ESP32 publish ke Mosquitto → perintah ini subscribe → simpan ke MySQL.
 * Mosquitto hanya broker pesan; tanpa subscriber, data tidak masuk database.
 */
class MqttListenCommand extends Command
{
    protected $signature = 'mqtt:listen
                            {--host= : Host Mosquitto (default dari .env)}
                            {--port= : Port Mosquitto (default 1883)}
                            {--topic= : Topic telemetry}';

    protected $description = 'Subscribe MQTT telemetry dari ESP32 dan simpan ke MySQL';

    public function handle(): int
    {
        $host = $this->option('host') ?: config('iot.mqtt_host', '127.0.0.1');
        $port = (int) ($this->option('port') ?: config('iot.mqtt_port', 1883));
        $topic = $this->option('topic') ?: config('iot.topic_telemetry');
        $username = (string) config('iot.mqtt_user', '');
        $password = (string) config('iot.mqtt_password', '');
        $clientId = 'laravel-mqtt-sub-'.getmypid();

        $this->info('=== Laravel MQTT Subscriber ===');
        $this->line("Broker : {$host}:{$port}");
        $this->line("Topic  : {$topic}");
        $this->line('Menunggu pesan dari ESP32... (Ctrl+C untuk stop)');

        $settings = (new ConnectionSettings)
            ->setKeepAliveInterval(60)
            ->setConnectTimeout(10)
            ->setUseTls(false);

        if ($username !== '') {
            $settings = $settings
                ->setUsername($username)
                ->setPassword($password);
        }

        try {
            $mqtt = new MqttClient($host, $port, $clientId);
            $mqtt->connect($settings, true);
        } catch (\Throwable $e) {
            $this->error('Gagal connect ke Mosquitto: '.$e->getMessage());
            $this->warn('Pastikan Mosquitto Start, dan host/port di .env benar.');

            return self::FAILURE;
        }

        $mqtt->subscribe($topic, function (string $topic, string $message) {
            $this->line("[MQTT] {$topic} ← {$message}");

            $payload = json_decode($message, true);
            if (! is_array($payload)) {
                $this->warn('JSON tidak valid, dilewati');

                return;
            }

            // Token opsional di payload — sama seperti API HTTP
            $token = $payload['token'] ?? null;
            $expected = config('iot.api_token');
            if (! is_string($token) || ! hash_equals((string) $expected, $token)) {
                $this->warn('Token invalid/missing — data ditolak');

                return;
            }

            if (! isset($payload['device_id'], $payload['temp'], $payload['hum'], $payload['seq'])) {
                $this->warn('Field wajib kurang (device_id/temp/hum/seq)');

                return;
            }

            $row = Telemetry::create([
                'device_id' => (string) $payload['device_id'],
                'fw' => (string) ($payload['fw'] ?? 'unknown'),
                'temp' => (float) $payload['temp'],
                'hum' => (float) $payload['hum'],
                'seq' => (int) $payload['seq'],
                'device_ts' => isset($payload['ts']) ? (int) $payload['ts'] : null,
                'source' => 'mqtt',
            ]);

            $this->info("[DB] tersimpan id={$row->id} temp={$row->temp} hum={$row->hum} seq={$row->seq}");
        }, 0);

        // loop forever — proses ini harus tetap hidup saat demo
        $mqtt->loop(true);

        return self::SUCCESS;
    }
}
