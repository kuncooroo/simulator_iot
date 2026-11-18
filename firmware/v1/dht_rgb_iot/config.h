#pragma once

// === WAJIB diganti sesuai WiFi & IP PC teman (lihat docs/04_install_mqtt_mosquitto.md) ===
#define WIFI_SSID     "NAMA_WIFI_KAMU"
#define WIFI_PASSWORD "PASSWORD_WIFI_KAMU"

#define DEVICE_ID     "esp32-dht-rgb-01"
#define API_TOKEN     "iot-simple-token-2026"

// IP PC tempat Mosquitto + Laravel jalan (hasil ipconfig), BUKAN 127.0.0.1
#define MQTT_HOST     "192.168.1.14"
#define MQTT_PORT     1883
// Kosongkan jika mosquitto.conf: allow_anonymous true
#define MQTT_USER     ""
#define MQTT_PASS     ""

// HTTP hanya untuk OTA download firmware (bukan telemetry)
#define HTTP_BASE_URL "http://192.168.1.14:8000"
#define OTA_URL_V2    "http://192.168.1.14:8000/api/ota/firmware_v2.bin"

#define PIN_DHT       4
#define PIN_LED_R     25  // LED merah
#define PIN_LED_G     26  // LED hijau
#define PIN_LED_Y     27  // LED kuning
