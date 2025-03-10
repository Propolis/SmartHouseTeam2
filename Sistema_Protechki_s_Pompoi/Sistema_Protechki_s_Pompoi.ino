#define RAIN_SENSOR_PIN 35  // Датчик протечки (MH-RD) на GPIO35 (D35)
#define PUMP_PIN 4  // Реле для управления помпой на GPIO4 (D4)

#define RAIN_THRESHOLD 3000  // Порог срабатывания (чем ниже, тем больше воды)

void setup() {
    pinMode(PUMP_PIN, OUTPUT);  // Настраиваем реле для помпы
    Serial.begin(115200);
    Serial.println("🚀 Система контроля протечки запущена");
}

void loop() {
    int rainValue = analogRead(RAIN_SENSOR_PIN);  // Читаем уровень воды

    Serial.print("🌊 Уровень воды: ");
    Serial.println(rainValue);

    if (rainValue < RAIN_THRESHOLD) {  
        Serial.println("⚠️ ПРОТЕЧКА ОБНАРУЖЕНА! ВЫКЛЮЧАЮ ПОМПУ!");
        digitalWrite(PUMP_PIN, LOW);  // Отключаем реле (и помпу)
    } else {
        Serial.println("✅ ПРОТЕЧКИ НЕТ. ПОМПА РАБОТАЕТ!");
        digitalWrite(PUMP_PIN, HIGH);  // Включаем реле (и помпу)
    }

    delay(1000);  // Проверяем каждую секунду
}
