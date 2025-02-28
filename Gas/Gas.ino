#define GAS_SENSOR_PIN 32  // Датчик дыма MQ-2 на GPIO35 (D35)

// Пороговое значение, при котором считается, что есть дым
#define SMOKE_THRESHOLD 900  //значение 900 с первого раза работает, но более реально значение - 2000, но это надо максимально близко подносить зажигалку

void setup() {
    Serial.begin(115200);  // Запускаем Serial Monitor
    Serial.println("🚀 Система детекции дыма запущена...");
}

void loop() {
    int gasValue = analogRead(GAS_SENSOR_PIN);  // Читаем уровень газа

    Serial.print("🔥 Уровень газа: ");
    Serial.println(gasValue);

    if (gasValue > SMOKE_THRESHOLD) {  
        Serial.println("⚠️ ДЕТЕКЦИЯ ДЫМА! ОПАСНО!");
    } else {
        Serial.println("✅ Дым не обнаружен.");
    }

    delay(1000);  // Читаем раз в секунду
}
