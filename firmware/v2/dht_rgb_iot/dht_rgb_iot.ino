/**
 * Firmware v2 — DHT11 + LED Merah/Hijau/Kuning (OTA target)
 * Perubahan vs v1:
 *  - Interval kirim: 3000 ms
 *  - Rule LED lebih ketat: hijau <24 | kuning 24–28 | merah >28
 * Pin: 25=merah, 26=hijau, 27=kuning (LED terpisah)
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <HTTPUpdate.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include "config.h"

#define FW_VERSION "2.0.0"
#define TELEMETRY_INTERVAL_MS 3000

DHT dht(PIN_DHT, DHT11);
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

unsigned long lastTelemetryMs = 0;
unsigned long seq = 0;
bool wifiWasConnected = false;

String topicTelemetry() {
  return String("smarthome/") + DEVICE_ID + "/telemetry";
}

String topicCommand() {
  return String("smarthome/") + DEVICE_ID + "/command";
}

// Satu LED nyala per kondisi (merah / hijau / kuning terpisah)
void setLeds(bool merah, bool hijau, bool kuning) {
  digitalWrite(PIN_LED_R, merah ? HIGH : LOW);
  digitalWrite(PIN_LED_G, hijau ? HIGH : LOW);
  digitalWrite(PIN_LED_Y, kuning ? HIGH : LOW);
}

void applyTempLedRule(float tempC) {
  if (isnan(tempC)) {
    // DHT error: semua mati
    setLeds(false, false, false);
    return;
  }
  if (tempC < 24.0) {
    setLeds(false, true, false);   // hijau
  } else if (tempC <= 28.0) {
    setLeds(false, false, true);   // kuning
  } else {
    setLeds(true, false, false);   // merah
  }
}

void connectWifi() {
  if (WiFi.status() == WL_CONNECTED) return;

  Serial.println("[WIFI] Connecting...");
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 20000) {
    delay(400);
    Serial.print(".");
  }
  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("[WIFI] connected");
    Serial.print("[WIFI] IP: ");
    Serial.println(WiFi.localIP());
    wifiWasConnected = true;
  } else {
    Serial.println("[WIFI] connect failed, will retry");
  }
}

bool authorizeToken(const char* token) {
  if (token == nullptr) return false;
  return String(token) == String(API_TOKEN);
}

void performOtaUpdate() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[OTA] abort: WiFi not connected");
    return;
  }
  Serial.println("[OTA] Starting HTTP OTA update...");
  WiFiClient client;
  t_httpUpdate_return ret = httpUpdate.update(client, OTA_URL_V2);
  switch (ret) {
    case HTTP_UPDATE_FAILED:
      Serial.printf("[OTA] Failed: %s\n", httpUpdate.getLastErrorString().c_str());
      break;
    case HTTP_UPDATE_NO_UPDATES:
      Serial.println("[OTA] No updates");
      break;
    case HTTP_UPDATE_OK:
      Serial.println("[OTA] OK — rebooting");
      break;
  }
}

void handleCommand(char* payload) {
  StaticJsonDocument<256> doc;
  DeserializationError err = deserializeJson(doc, payload);
  if (err) {
    Serial.println("[CMD] invalid json — rejected");
    return;
  }

  const char* token = doc["token"];
  if (!authorizeToken(token)) {
    Serial.println("[SEC] REJECT unauthorized command");
    return;
  }

  const char* action = doc["action"] | "";
  if (String(action) == "ota_update") {
    Serial.println("[OTA] Authorized OTA request received");
    performOtaUpdate();
  } else if (String(action) == "ping") {
    Serial.println("[CMD] ping ok");
  } else {
    Serial.println("[CMD] unknown action");
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  char buf[512];
  if (length >= sizeof(buf)) length = sizeof(buf) - 1;
  memcpy(buf, payload, length);
  buf[length] = '\0';
  handleCommand(buf);
}

void connectMqtt() {
  if (mqtt.connected()) return;
  if (WiFi.status() != WL_CONNECTED) return;

  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  mqtt.setCallback(mqttCallback);

  String clientId = String(DEVICE_ID) + "-v2";
  Serial.println("[MQTT] Connecting...");
  bool ok;
  if (String(MQTT_USER).length() == 0) {
    ok = mqtt.connect(clientId.c_str());
  } else {
    ok = mqtt.connect(clientId.c_str(), MQTT_USER, MQTT_PASS);
  }
  if (ok) {
    Serial.println("[MQTT] connected");
    mqtt.subscribe(topicCommand().c_str());
  } else {
    Serial.print("[MQTT] failed rc=");
    Serial.println(mqtt.state());
  }
}

void ensureConnectivity() {
  if (WiFi.status() != WL_CONNECTED) {
    if (wifiWasConnected) {
      Serial.println("[WIFI] disconnected — auto-reconnect...");
    }
    connectWifi();
  }
  if (WiFi.status() == WL_CONNECTED && !mqtt.connected()) {
    Serial.println("[MQTT] reconnecting...");
    connectMqtt();
  }
}

void publishTelemetry(float tempC, float hum) {
  // Telemetry hanya lewat MQTT (hardware real → broker → bridge → Laravel/MySQL)
  if (!mqtt.connected()) {
    Serial.println("[TEL] skip: MQTT not connected");
    return;
  }

  seq++;
  StaticJsonDocument<256> doc;
  doc["device_id"] = DEVICE_ID;
  doc["fw"] = FW_VERSION;
  doc["temp"] = tempC;
  doc["hum"] = hum;
  doc["seq"] = seq;
  doc["ts"] = (uint32_t)(millis() / 1000);
  doc["source"] = "mqtt";
  doc["token"] = API_TOKEN;

  char body[256];
  serializeJson(doc, body, sizeof(body));

  bool ok = mqtt.publish(topicTelemetry().c_str(), body, false);
  Serial.print("[TEL] MQTT seq=");
  Serial.print(seq);
  Serial.print(" temp=");
  Serial.print(tempC);
  Serial.print(" hum=");
  Serial.print(hum);
  Serial.println(ok ? " OK" : " FAIL");
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println();
  Serial.println("=== DHT LED IoT FW v2.0.0 (OTA) ===");
  Serial.print("Device: ");
  Serial.println(DEVICE_ID);
  Serial.println("Interval=3000ms | LED rule stricter");

  pinMode(PIN_LED_R, OUTPUT);
  pinMode(PIN_LED_G, OUTPUT);
  pinMode(PIN_LED_Y, OUTPUT);
  setLeds(false, false, false);

  dht.begin();
  connectWifi();
  connectMqtt();
}

void loop() {
  ensureConnectivity();
  if (mqtt.connected()) mqtt.loop();

  unsigned long now = millis();
  if (now - lastTelemetryMs >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryMs = now;
    float hum = dht.readHumidity();
    float tempC = dht.readTemperature();

    if (isnan(hum) || isnan(tempC)) {
      Serial.println("[DHT] read failed");
      applyTempLedRule(NAN);
    } else {
      Serial.print("[DHT] temp=");
      Serial.print(tempC);
      Serial.print("C hum=");
      Serial.print(hum);
      Serial.println("%");
      applyTempLedRule(tempC);
      publishTelemetry(tempC, hum);
    }
  }
}
