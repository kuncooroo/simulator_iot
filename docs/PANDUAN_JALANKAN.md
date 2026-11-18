# Panduan Menjalankan — Hardware + MQTT + Laravel 11 (PHP 8.2)

**Folder project:** `...\Simple_IoT_Laravel\`  
**PHP:** ^8.2 (contoh teman: **8.2.29** OK)  
**Laravel:** 11  
**Port API:** 8000 · **MQTT:** 1883  
**DB:** MySQL `iot_simple_laravel`  
**Token:** `iot-simple-token-2026`

Baca penjelasan konsep dulu: **[05_penjelasan_mqtt_dan_subscriber.md](05_penjelasan_mqtt_dan_subscriber.md)**

---

## A. Software yang dibutuhkan

| Software | Versi / catatan |
|----------|-----------------|
| PHP | **8.2.x** (atau 8.3+) — cek `php -v` |
| Composer | untuk `composer install` |
| MySQL (Laragon) | database |
| Mosquitto | broker MQTT — lihat [04_install_mqtt_mosquitto.md](04_install_mqtt_mosquitto.md) |
| Arduino IDE + board ESP32 | upload firmware |
| Library: DHT, PubSubClient, ArduinoJson | compile sketch |

> Project ini **sudah di-lock** ke platform PHP `8.2.29` di `composer.json`, jadi `composer install` di PC teman (PHP 8.2.29) seharusnya lolos.

---

## B. Setup sekali — Laravel + MySQL

1. Start **MySQL** di Laragon.  
2. Buat DB:

```powershell
mysql -uroot -e "CREATE DATABASE IF NOT EXISTS iot_simple_laravel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

(atau lewat HeidiSQL / phpMyAdmin)

3. Masuk folder Laravel:

```powershell
cd G:\Mahen\Downloads\Simple_IoT_Laravel\Simple_IoT_Laravel\platform\laravel
composer install
copy .env.example .env
php artisan key:generate
```

4. Pastikan `.env` berisi:

```env
DB_CONNECTION=mysql
DB_DATABASE=iot_simple_laravel
DB_USERNAME=root
DB_PASSWORD=

IOT_API_TOKEN=iot-simple-token-2026
IOT_MQTT_HOST=127.0.0.1
IOT_MQTT_PORT=1883
```

5. Migrate:

```powershell
php artisan migrate
php artisan db:show
```

---

## C. Firmware ESP32

1. Wiring: [01_wiring.md](01_wiring.md)  
2. `ipconfig` → catat IPv4 PC, contoh `192.168.1.14`  
3. Edit `firmware/v1/dht_rgb_iot/config.h` (dan v2):

```cpp
#define WIFI_SSID     "NAMA_WIFI"
#define WIFI_PASSWORD "PASSWORD"

#define MQTT_HOST     "192.168.1.14"  // IP PC Mosquitto — JANGAN 127.0.0.1
#define MQTT_PORT     1883
#define MQTT_USER     ""
#define MQTT_PASS     ""

#define HTTP_BASE_URL "http://192.168.1.14:8000"
#define OTA_URL_V2    "http://192.168.1.14:8000/api/ota/firmware_v2.bin"
```

4. Upload **v1**, Serial Monitor **115200** → cari `[WIFI] connected` dan `[MQTT] connected`.

---

## D. Urutan jalankan setiap demo

### 0) Start service

- Laragon MySQL **Start**
- Mosquitto Broker **Start** (lihat doc 04)

### 1) Terminal A — Laravel web/API

```powershell
cd ...\platform\laravel
php artisan serve --host=0.0.0.0 --port=8000
```

Cek: http://127.0.0.1:8000/api/health  
Dashboard: http://127.0.0.1:8000/

### 2) Terminal B — Subscriber MQTT (penting!)

```powershell
cd ...\platform\laravel
php artisan mqtt:listen
```

Harus muncul: `Menunggu pesan dari ESP32...`

Tanpa terminal ini, data MQTT **tidak masuk MySQL**.

### 3) Nyalakan ESP32

Jika Serial `[TEL] MQTT ... OK` dan terminal B mencetak `[DB] tersimpan ...` → dashboard update.

---

## E. OTA v1 → v2

Lihat [03_sop_ota.md](03_sop_ota.md). Ringkas:

```powershell
cd "C:\Program Files\mosquitto"
.\mosquitto_pub.exe -h 127.0.0.1 -t "smarthome/esp32-dht-rgb-01/command" -m "{\"action\":\"ota_update\",\"token\":\"iot-simple-token-2026\"}"
```

---

## F. Uji cepat

| Uji | Hasil |
|-----|-------|
| `php -v` | 8.2.x |
| `composer install` | sukses tanpa error PHP version |
| `/api/health` | status ok |
| `mqtt:listen` + ESP32 | baris `[DB] tersimpan` |
| Dashboard | suhu/RH berubah |
| MySQL `source` | `mqtt` |

---

## G. Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `requires php ^8.3` | Pastikan pakai **zip project terbaru** (Laravel 11). Jangan pakai folder Laravel 13 lama. |
| MySQL refused | Start MySQL Laragon |
| `mqtt:listen` gagal connect | Mosquitto belum Start / port 1883 |
| ESP32 MQTT fail | IP di `config.h` salah / firewall 1883 |
| Dashboard kosong | Lupa jalankan `php artisan mqtt:listen` |
