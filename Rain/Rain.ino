#define RAIN_SENSOR_PIN 35  // Датчик дождя на GPIO35 (D35)

// Пороговое значение дождя (можно настроить под условия)
#define RAIN_THRESHOLD 2000  // Чем ниже, тем больше воды

void setup() {
    Serial.begin(115200);  // Запускаем Serial Monitor
    Serial.println("🚀 Система дождя запущена...");
}

void loop() {
    int rainValue = analogRead(RAIN_SENSOR_PIN);  // Читаем уровень дождя

    Serial.print("🌧 Уровень дождя: ");
    Serial.println(rainValue);

    if (rainValue < RAIN_THRESHOLD) {  
        Serial.println("⚠️ Дождь обнаружен!");
    } else {
        Serial.println("✅ Нет дождя.");
    }

    delay(1000);  // Читаем раз в секунду
}
