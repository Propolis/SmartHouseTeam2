#include <WiFi.h>
#include <PubSubClient.h>

// Настройки WiFi
const char* ssid = "Tochka";
const char* password = "password";

// Настройки MQTT
const char* mqtt_server = "m1.wqtt.ru";
const int mqtt_port = 13010;
const char* mqtt_user = "u_TNQXY5";
const char* mqtt_pass = "6En7SeKP";
const char* mqtt_topic_lamp = "Lamp1";
const char* mqtt_topic_rgb = "RGB1"; // Топик для управления RGB светодиодом

// Пины для RGB светодиода
const int redPin = 4;
const int greenPin = 2;
const int bluePin = 15;

// Уникальный ID клиента MQTT
String clientId = "ESP32Client-" + String(random(0xffff), HEX);

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Подключение к WiFi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi подключен");
  Serial.print("IP адрес: ");
  Serial.println(WiFi.localIP());
}

// Функция для установки цвета RGB светодиода
void setColor(int red, int green, int blue) {
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);
}

// Функция для обработки RGB-команд в формате "R,G,B"
void setColorFromRGB(String rgb) {
  int commaIndex1 = rgb.indexOf(',');
  int commaIndex2 = rgb.indexOf(',', commaIndex1 + 1);

  if (commaIndex1 != -1 && commaIndex2 != -1) {
    int r = rgb.substring(0, commaIndex1).toInt();
    int g = rgb.substring(commaIndex1 + 1, commaIndex2).toInt();
    int b = rgb.substring(commaIndex2 + 1).toInt();

    setColor(r, g, b);
    Serial.print("Установлен цвет RGB: ");
    Serial.print(r);
    Serial.print(",");
    Serial.print(g);
    Serial.print(",");
    Serial.println(b);
  } else {
    Serial.println("Некорректный формат RGB-команды.");
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Получено сообщение в топик: ");
  Serial.print(topic);
  Serial.print(", сообщение: ");
  
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  if (String(topic) == mqtt_topic_lamp) {
    // Управление включением/выключением
    if (message == "1") {
      setColor(255, 255, 255); // Белый цвет по умолчанию при включении
      Serial.println("RGB светодиод включен (белый)");
    } else if (message == "0") {
      setColor(0, 0, 0); // Выключить светодиод
      Serial.println("RGB светодиод выключен");
    } else {
      Serial.println("Получена неизвестная команда.");
    }
  } else if (String(topic) == mqtt_topic_rgb) {
    // Управление цветом RGB через формат "R,G,B"
    setColorFromRGB(message);
  }
}

void reconnect() {
  int attempts = 0;
  while (!client.connected() && attempts < 5) {
    attempts++;
    Serial.print("Попытка подключения к MQTT #");
    Serial.print(attempts);
    Serial.print(" ...");
    
    if (client.connect(clientId.c_str(), mqtt_user, mqtt_pass)) {
      Serial.println("Подключено!");
      if (client.subscribe(mqtt_topic_lamp) && client.subscribe(mqtt_topic_rgb)) {
        Serial.println("Успешно подписан на топики!");
      } else {
        Serial.println("Ошибка подписки на топики.");
      }
    } else {
      Serial.print("Ошибка подключения, rc=");
      Serial.print(client.state());
      Serial.println(" Повтор через 5 секунд...");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  
  Serial.begin(115200);
  setup_wifi();
  
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  
  Serial.println("Настройка завершена, пытаемся подключиться к MQTT...");
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  
  client.loop();
  delay(10);
}
