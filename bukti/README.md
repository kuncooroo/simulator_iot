# Folder screenshot presentasi

Ambil SS lalu simpan dengan **nama file persis** di bawah.  
Setelah lengkap, regenerate PPT:

```powershell
cd D:\Tugas_Akhir\Simple_IoT_Laravel\laporan
python buat_ppt_presentasi.py
```

Atau tempel manual ke kotak "SLOT SCREENSHOT" di PowerPoint.

| File | Isi SS |
|------|--------|
| `debug/01_persiapan_mosquitto_ip.png` | Mosquitto Running + ipconfig |
| `dashboard/01_health_atau_serve.png` | `artisan serve` + `/api/health` |
| `mqtt_listen/01_mqtt_listen_ready.png` | Terminal `mqtt:listen` siap |
| `serial/01_esp32_mqtt_ok.png` | Serial `[MQTT] connected` |
| `serial/02_telemetry_ok.png` | Serial `[TEL] ... OK` |
| `mqtt_listen/02_db_tersimpan.png` | `[DB] tersimpan` |
| `dashboard/02_dashboard_live.png` | Dashboard grafik hidup |
| `debug/02_listen_off_serial_ok.png` | Serial tetap OK saat listen off |
| `mqtt_listen/03_token_reject.png` | Token invalid/missing |
| `ota/01_ota_serial.png` | OTA / fw 2.0.0 |
