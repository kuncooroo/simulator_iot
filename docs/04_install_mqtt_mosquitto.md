# Cara Download & Pasang MQTT (Mosquitto) — Windows

MQTT di project ini memakai **Eclipse Mosquitto** sebagai *broker* (server pesan).  
ESP32 **publish** data suhu/RH ke Mosquitto. Bridge lalu meneruskan ke Laravel → MySQL.

---

## Apa itu MQTT (singkat)

| Istilah | Artinya |
|---------|---------|
| Broker | Server MQTT (Mosquitto) di PC |
| Publish | ESP32 mengirim pesan ke topic |
| Subscribe | Bridge / tools membaca pesan dari topic |
| Topic | Alamat pesan, contoh: `smarthome/esp32-dht-rgb-01/telemetry` |
| Port | Default **1883** (tanpa TLS) |

Alur project:

```
ESP32 (hardware)  --publish-->  Mosquitto  --subscribe-->  php artisan mqtt:listen  -->  MySQL
                                                                      (di dalam Laravel)
```

> Mosquitto **bukan** database. Ia hanya broker.  
> Yang menyimpan ke MySQL adalah perintah Laravel: `php artisan mqtt:listen`.  
> Baca penjelasan lengkap: [05_penjelasan_mqtt_dan_subscriber.md](05_penjelasan_mqtt_dan_subscriber.md)

---

## 1) Download Mosquitto

1. Buka situs resmi: https://mosquitto.org/download/
2. Pilih bagian **Windows**.
3. Download installer 64-bit, contoh nama file:
   - `mosquitto-2.0.xx-install-windows-x64.exe`
4. Atau unduh langsung dari mirror GitHub Eclipse Mosquitto (Assets release):
   - https://github.com/eclipse/mosquitto/releases

---

## 2) Install di Windows

1. Jalankan file `.exe` installer.
2. Centang opsi:
   - **Service** (agar Mosquitto bisa jalan sebagai Windows Service)
   - **Mosquitto** / client tools (`mosquitto_pub`, `mosquitto_sub`)
3. Install ke folder default, biasanya:
   - `C:\Program Files\mosquitto\`
4. Selesai → Restart PC jika diminta (opsional, biasanya tidak wajib).

Cek sudah terpasang:

```powershell
& "C:\Program Files\mosquitto\mosquitto.exe" -h
```

Atau (jika PATH sudah ditambah):

```powershell
mosquitto -h
```

---

## 3) Konfigurasi agar ESP32 bisa connect dari WiFi

Buka (sebagai Administrator) file:

`C:\Program Files\mosquitto\mosquitto.conf`

Tambahkan / pastikan baris berikut ada (boleh di akhir file):

```conf
listener 1883
allow_anonymous true
```

Penjelasan:

- `listener 1883` → broker mendengar di port 1883 (semua interface / bisa dari LAN)
- `allow_anonymous true` → untuk demo lokal boleh tanpa username (lebih mudah untuk teman yang baru belajar)

> Untuk produksi sebaiknya pakai username/password. Untuk ujian/demo lokal, anonymous OK.

Simpan file.

---

## 4) Izinkan firewall Windows (penting)

ESP32 dan PC harus satu WiFi. Firewall sering memblokir port 1883.

PowerShell **Run as Administrator**:

```powershell
New-NetFirewallRule -DisplayName "Mosquitto MQTT 1883" -Direction Inbound -Protocol TCP -LocalPort 1883 -Action Allow
```

---

## 5) Menjalankan Mosquitto

### Cara A — Service (paling mudah)

1. Tekan `Win + R` → ketik `services.msc` → Enter.
2. Cari **Mosquitto Broker**.
3. Klik kanan → **Start** (atau set Startup type = Automatic).

### Cara B — Terminal manual

```powershell
cd "C:\Program Files\mosquitto"
.\mosquitto.exe -c mosquitto.conf -v
```

Flag `-v` = verbose (lihat log connect/publish). Biarkan terminal ini tetap terbuka.

---

## 6) Uji broker sudah hidup

Buka **2 terminal**.

**Terminal A — subscribe (mendengarkan):**

```powershell
cd "C:\Program Files\mosquitto"
.\mosquitto_sub.exe -h 127.0.0.1 -t "smarthome/esp32-dht-rgb-01/telemetry" -v
```

**Terminal B — publish uji:**

```powershell
cd "C:\Program Files\mosquitto"
.\mosquitto_pub.exe -h 127.0.0.1 -t "smarthome/esp32-dht-rgb-01/telemetry" -m "{\"temp\":26.5,\"hum\":60,\"seq\":1}"
```

Jika Terminal A menampilkan pesan JSON → **MQTT sudah OK**.

---

## 7) Samakan IP di firmware

Di PC, cek IP WiFi:

```powershell
ipconfig
```

Cari `IPv4 Address` adapter WiFi, contoh `192.168.1.14`.

Edit file firmware:

`firmware/v1/dht_rgb_iot/config.h` (dan v2):

```cpp
#define MQTT_HOST     "192.168.1.14"   // IP PC tempat Mosquitto jalan
#define MQTT_PORT     1883
#define MQTT_USER     ""               // kosong jika allow_anonymous true
#define MQTT_PASS     ""
#define HTTP_BASE_URL "http://192.168.1.14:8000"  // untuk OTA saja
#define OTA_URL_V2    "http://192.168.1.14:8000/api/ota/firmware_v2.bin"
```

Upload ulang firmware ke ESP32.

---

## 8) Subscriber MQTT di Laravel (wajib saat demo)

Laravel web (`php artisan serve`) **tidak otomatis** mendengar MQTT.  
Jalankan subscriber di terminal terpisah:

```powershell
cd ...\platform\laravel
php artisan mqtt:listen
```

Ini connect ke `IOT_MQTT_HOST` (biasanya `127.0.0.1` jika Mosquitto di PC yang sama).  
ESP32 tetap connect ke **IP LAN PC** di `config.h` (`MQTT_HOST`).

---

## 9) Kirim perintah OTA lewat MQTT

Setelah firmware v1 jalan dan Laravel menyajikan `firmware_v2.bin`:

```powershell
cd "C:\Program Files\mosquitto"
.\mosquitto_pub.exe -h 127.0.0.1 -t "smarthome/esp32-dht-rgb-01/command" -m "{\"action\":\"ota_update\",\"token\":\"iot-simple-token-2026\"}"
```

Serial Monitor ESP32 harus muncul `[OTA] Authorized...`.

---

## Troubleshooting MQTT

| Gejala | Penyebab umum | Perbaikan |
|--------|---------------|-----------|
| ESP32 `[MQTT] failed rc=...` | Broker mati / IP salah | Start Mosquitto, cek `MQTT_HOST` = IP PC |
| rc=5 / auth error | User/pass tidak cocok | Samakan `MQTT_USER`/`PASS` atau `allow_anonymous true` |
| Connect dari PC OK, dari ESP32 gagal | Firewall | Buka port 1883 inbound |
| `mqtt:listen` diam saja | Topic beda / ESP32 belum publish | Samakan topic; cek Serial ESP32 |
| Data MQTT ada, dashboard kosong | Subscriber belum jalan | Jalankan `php artisan mqtt:listen` + `serve` |

Kode `rc` PubSubClient yang sering muncul:

- `-2` / `MQTT_CONNECT_FAILED` → WiFi/IP/port
- `4` → bad username/password
- `5` → not authorized

---

## Checklist sebelum demo hardware

- [ ] Mosquitto terpasang & **Start**
- [ ] `mosquitto.conf` punya `listener 1883` + `allow_anonymous true`
- [ ] Firewall port **1883** dibuka
- [ ] `mosquitto_sub` / `mosquitto_pub` uji lokal berhasil
- [ ] `config.h` memakai IP PC yang benar
- [ ] Laravel + MySQL jalan (`php artisan serve`)
- [ ] `php artisan mqtt:listen` jalan
- [ ] ESP32 Serial: `[WIFI] connected` lalu `[MQTT] connected`
- [ ] Dashboard http://127.0.0.1:8000/ menampilkan suhu/RH
