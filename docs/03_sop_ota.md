# SOP OTA Firmware v1 → v2 (MQTT + hardware)

## Perbedaan v1 vs v2

| Item | v1 | v2 |
|------|----|----|
| Version | 1.0.0 | 2.0.0 |
| Interval | 5000 ms | 3000 ms |
| LED rule | LED terpisah: &lt;25 hijau, 25–30 kuning, &gt;30 merah | LED terpisah: &lt;24 hijau, 24–28 kuning, &gt;28 merah |

## Langkah

1. Pastikan ESP32 sudah jalan dengan **firmware v1** (USB upload).
2. Di Arduino IDE, buka sketch **v2**, **Sketch → Export compiled Binary**.
3. Salin file `.bin` hasil export ke:
   `platform/laravel/storage/app/ota/firmware_v2.bin`
   (timpa placeholder).
4. Laravel harus jalan; cek: http://127.0.0.1:8000/api/ota/info
5. Pastikan `OTA_URL_V2` di `config.h` mengarah ke **IP PC** (bukan `127.0.0.1` dari sudut ESP32).
6. Trigger OTA lewat MQTT (Mosquitto):

```powershell
cd "C:\Program Files\mosquitto"
.\mosquitto_pub.exe -h 127.0.0.1 -t "smarthome/esp32-dht-rgb-01/command" -m "{\"action\":\"ota_update\",\"token\":\"iot-simple-token-2026\"}"
```

Payload yang dikirim:

```json
{"action":"ota_update","token":"iot-simple-token-2026"}
```

7. Serial Monitor 115200: `[OTA] Authorized...` → download → reboot.
8. Setelah reboot, pesan telemetry memuat `"fw":"2.0.0"` (interval lebih cepat).

## Catatan keamanan

- Tanpa token / token salah → ESP32 menolak command (`[SEC] REJECT`).
- Placeholder `.bin` di repo **tidak** bisa di-flash sebagai firmware nyata; wajib diganti hasil compile v2.

## Ingat saat demo OTA

- `php artisan serve` harus hidup (ESP32 unduh `.bin` via HTTP).
- `php artisan mqtt:listen` boleh tetap hidup untuk telemetry.
- Perintah OTA dikirim lewat **Mosquitto** (`mosquitto_pub`), bukan lewat tombol dashboard saja.
