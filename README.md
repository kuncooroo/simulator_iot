# Simple IoT Hardware — DHT + RGB + MQTT → Laravel + MySQL

Project **hardware nyata** untuk monitoring suhu/kelembapan:

- ESP32 + **DHT11** + **LED RGB**
- Telemetry lewat **MQTT (Mosquitto)**
- Subscriber **langsung di Laravel** (`php artisan mqtt:listen`) → MySQL
- Dashboard Blade + OTA v1 → v2

**Kompatibel PHP 8.2** (Laravel 11) — cocok untuk Laragon teman yang masih PHP 8.2.29.

## Baca berurutan

1. **[docs/05_penjelasan_mqtt_dan_subscriber.md](docs/05_penjelasan_mqtt_dan_subscriber.md)** — *kenapa* Mosquitto + subscriber Laravel  
2. **[docs/04_install_mqtt_mosquitto.md](docs/04_install_mqtt_mosquitto.md)** — cara pasang Mosquitto  
3. **[docs/PANDUAN_JALANKAN.md](docs/PANDUAN_JALANKAN.md)** — urutan jalankan  
4. **[docs/01_wiring.md](docs/01_wiring.md)** · **[docs/03_sop_ota.md](docs/03_sop_ota.md)**

## Perintah cepat

```powershell
# Terminal 1 — Laravel API + dashboard
cd ...\platform\laravel
composer install
php artisan migrate
php artisan serve --host=0.0.0.0 --port=8000

# Terminal 2 — Subscriber MQTT (WAJIB saat demo)
php artisan mqtt:listen

# Terminal 3 — ESP32 sudah di-upload firmware v1 (Serial 115200)
```

Syarat: MySQL Start + Mosquitto Start.

- Dashboard: http://127.0.0.1:8000/  
- Token: `iot-simple-token-2026`  
- DB: `iot_simple_laravel`  
- PHP: **^8.2** (Laravel 11)

## Struktur

```
Simple_IoT_Laravel/
├── platform/laravel     # Laravel 11 + mqtt:listen + dashboard
├── firmware/v1 & v2     # ESP32 hardware
├── docs/                # Penjelasan + panduan
└── README.md
```

Tidak ada simulator. Tidak ada bridge Python.
