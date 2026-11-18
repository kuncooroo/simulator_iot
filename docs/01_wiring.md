# Wiring ESP32 — DHT11 + LED Merah / Hijau / Kuning

## Komponen

- ESP32 DevKit
- DHT11
- LED **merah**, **hijau**, **kuning** (terpisah, bukan modul RGB)
- Resistor 4.7k–10k (pull-up DHT)
- Resistor ~220Ω untuk tiap LED
- Kabel jumper + breadboard

## Pin

| Komponen | Pin ESP32 | Keterangan |
|----------|-----------|------------|
| DHT DATA | GPIO **4** | + pull-up ke 3.3V |
| DHT VCC | **3.3V** | |
| DHT GND | **GND** | |
| LED **Merah** | GPIO **25** | + resistor ~220Ω → GND |
| LED **Hijau** | GPIO **26** | + resistor ~220Ω → GND |
| LED **Kuning** | GPIO **27** | + resistor ~220Ω → GND |

```
ESP32 GPIO25 ──[220Ω]──► LED Merah  ──► GND
ESP32 GPIO26 ──[220Ω]──► LED Hijau  ──► GND
ESP32 GPIO27 ──[220Ω]──► LED Kuning ──► GND
ESP32 GPIO4  ──────────► DHT DATA (+ pull-up ke 3.3V)
```

## Logic LED

Hanya **satu** LED yang nyala:

| Kondisi (v1) | LED |
|--------------|-----|
| DHT gagal | semua mati |
| suhu &lt; 25°C | hijau |
| 25–30°C | kuning |
| &gt; 30°C | merah |

| Kondisi (v2) | LED |
|--------------|-----|
| DHT gagal | semua mati |
| suhu &lt; 24°C | hijau |
| 24–28°C | kuning |
| &gt; 28°C | merah |

## Alur setelah wiring

```
DHT baca suhu/RH → ESP32 → publish MQTT → Mosquitto → php artisan mqtt:listen → MySQL
                 ↘ nyalakan 1 LED sesuai suhu
```

Lihat: [04_install_mqtt_mosquitto.md](04_install_mqtt_mosquitto.md) · [05_penjelasan_mqtt_dan_subscriber.md](05_penjelasan_mqtt_dan_subscriber.md)
