<?php

return [
    'api_token' => env('IOT_API_TOKEN', 'iot-simple-token-2026'),
    'device_id' => env('IOT_DEVICE_ID', 'esp32-dht-rgb-01'),
    'topic_telemetry' => env('IOT_TOPIC_TELEMETRY', 'smarthome/esp32-dht-rgb-01/telemetry'),
    'topic_command' => env('IOT_TOPIC_COMMAND', 'smarthome/esp32-dht-rgb-01/command'),

    // Broker Mosquitto — dipakai perintah: php artisan mqtt:listen
    'mqtt_host' => env('IOT_MQTT_HOST', '127.0.0.1'),
    'mqtt_port' => (int) env('IOT_MQTT_PORT', 1883),
    'mqtt_user' => env('IOT_MQTT_USER', ''),
    'mqtt_password' => env('IOT_MQTT_PASSWORD', ''),
];
