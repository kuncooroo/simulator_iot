# Penjelasan: Mosquitto vs Subscriber Laravel

Dokumen ini **bukan sekadar langkah klik**, tapi menjelaskan *kenapa* tiap komponen ada.

---

## 1) Analogi sederhana

Bayangkan sistem chat:

| Peran | Di project ini | Analogi |
|-------|----------------|---------|
| Pengirim | **ESP32** (DHT + RGB) | Orang yang kirim chat |
| Server chat | **Mosquitto** (broker MQTT) | WhatsApp Server / ruang pesan |
| Penerima yang menyimpan | **Laravel `mqtt:listen`** | Admin yang baca chat lalu catat ke buku/DB |
| Buku catatan | **MySQL** | Database |
| Papan info | **Dashboard** `/` | Layar yang menampilkan catatan |

Kalau hanya pasang Mosquitto:

- ESP32 bisa **kirim** pesan
- Pesan **ada di “udara” broker**
- Tapi **tidak ada yang mencatat ke MySQL** → dashboard kosong

Itulah kenapa butuh **subscriber** di Laravel.

---

## 2) Apa itu MQTT?

MQTT = protokol pesan ringan untuk IoT.

- **Publish**: mengirim pesan ke sebuah *topic* (alamat string)
- **Subscribe**: mendengarkan topic tertentu
- **Broker**: perantara (Mosquitto). Ia tidak menyimpan ke MySQL; ia hanya meneruskan pesan.

Topic di project ini:

- Telemetry: `smarthome/esp32-dht-rgb-01/telemetry`
- Command/OTA: `smarthome/esp32-dht-rgb-01/command`

---

## 3) Kenapa subscriber digabung di Laravel?

Dulu ada ide “bridge Python”. Sekarang **langsung di Laravel**:

```text
php artisan mqtt:listen
```

Perintah ini (file `app/Console/Commands/MqttListenCommand.php`):

1. Connect ke Mosquitto (`IOT_MQTT_HOST` / port 1883)
2. Subscribe topic telemetry
3. Setiap pesan JSON masuk → validasi token → `Telemetry::create(...)` ke MySQL
4. Dashboard membaca MySQL dan menampilkan grafik

Keuntungan untuk teman yang ujian:

- Tidak perlu Python / `paho-mqtt`
- Semua backend satu stack: **PHP + Laravel + MySQL**
- Cocok dijelaskan: “subscriber MQTT native di Laravel”

---

## 4) Alur lengkap (hafalkan untuk presentasi)

```
[Hardware ESP32]
   baca DHT → atur warna RGB
   publish JSON ke Mosquitto (topic telemetry)
           │
           ▼
[Mosquitto Broker :1883]
   hanya meneruskan pesan
           │
           ▼
[php artisan mqtt:listen]   ← subscriber Laravel
   parse JSON + cek token
   INSERT ke tabel telemetries (MySQL)
           │
           ▼
[Browser dashboard http://127.0.0.1:8000]
   tampil suhu / RH / grafik
```

OTA:

```
PC kirim mosquitto_pub (action=ota_update)
   → ESP32 subscribe command topic
   → ESP32 download firmware via HTTP Laravel /api/ota/firmware_v2.bin
   → reboot jadi v2
```

HTTP di firmware **hanya untuk unduh file OTA**, bukan untuk kirim telemetry.

---

## 5) File penting

| File | Fungsi |
|------|--------|
| `firmware/.../dht_rgb_iot.ino` | Publish MQTT + LED rule + OTA |
| `firmware/.../config.h` | WiFi, IP Mosquitto, URL OTA |
| `app/Console/Commands/MqttListenCommand.php` | Subscriber Laravel |
| `config/iot.php` + `.env` | Token, topic, host MQTT, DB |
| `app/Models/Telemetry.php` | Model MySQL |
| `resources/views/dashboard.blade.php` | UI monitoring |

---

## 6) Yang sering salah paham

1. **“Sudah install Mosquitto, kenapa dashboard kosong?”**  
   Karena belum jalankan `php artisan mqtt:listen`.

2. **“Laravel `serve` saja cukup?”**  
   Tidak. `serve` = API + dashboard. `mqtt:listen` = proses terpisah yang harus hidup terus saat demo.

3. **“Kenapa ESP32 tidak pakai 127.0.0.1?”**  
   `127.0.0.1` = dirinya sendiri. ESP32 harus isi **IP PC** di `MQTT_HOST`.

4. **“Token untuk apa?”**  
   Agar pesan palsu tanpa token tidak masuk DB / tidak memicu OTA.
