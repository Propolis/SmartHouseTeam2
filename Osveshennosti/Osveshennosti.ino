#define LIGHT_SENSOR_PIN 14  // Датчик освещённости TEMT6000 (аналоговый вход)
#define LED_PIN 2  // Светодиод подключен к GPIO2 (D2)

void setup() {
    pinMode(LIGHT_SENSOR_PIN, INPUT);
    pinMode(LED_PIN, OUTPUT);
    Serial.begin(115200);
    Serial.println("🚀 Датчик освещённости TEMT6000 запущен");
}

void loop() {
    int lightDigital = digitalRead(LIGHT_SENSOR_PIN);  // Читаем цифровой выход

    if (lightDigital == LOW) {  
        Serial.println("☀️ Очень светло!");
        digitalWrite(LED_PIN, LOW);  // Выключаем диод
    } else {
        Serial.println("🌑 Темно! Включаю свет!");
        digitalWrite(LED_PIN, HIGH);  // Включаем диод
    }

    delay(1000);  // Проверяем каждую секунду
}