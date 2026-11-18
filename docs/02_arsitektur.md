# Arsitektur — Hardware MQTT + Subscriber Laravel

```
┌─────────────────┐   publish telemetry    ┌──────────────────┐
│ ESP32 (nyata)   │ ─────────────────────► │ Mosquitto :1883  │
│ DHT11 + RGB     │ ◄───────────────────── │ (broker saja)    │
└────────┬────────┘   command / OTA MQTT   └────────┬─────────┘
         │                                          │
         │ HTTP hanya unduh OTA .bin                │ subscribe
         │                                          ▼
         │                             ┌────────────────────────────┐
         │                             │ php artisan mqtt:listen    │
         │                             │ (subscriber di Laravel)    │
         │                             └─────────────┬──────────────┘
         │                                           │ Eloquent insert
         ▼                                           ▼
┌────────────────────────────────────────────────────────────────────┐
│ Laravel 11 (:8000)  +  MySQL telemetries  +  Dashboard Blade       │
└────────────────────────────────────────────────────────────────────┘
```

## Penjelasan singkat

- **Mosquitto** = kurir pesan (tidak menulis database).
- **`mqtt:listen`** = petugas yang mendengar MQTT lalu menulis MySQL.
- **Dashboard** = membaca MySQL, bukan membaca MQTT langsung.

Detail konsep: [05_penjelasan_mqtt_dan_subscriber.md](05_penjelasan_mqtt_dan_subscriber.md)
