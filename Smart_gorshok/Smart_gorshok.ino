#define SOIL_SENSOR_PIN 2   // Датчик влажности почвы (Аналоговый вход)
#define RELAY_PIN 5         // Реле для насоса (Цифровой выход)

#define SOIL_THRESHOLD 2000  // Порог влажности (чем ниже, тем влажнее)

void setup() {
    pinMode(RELAY_PIN, OUTPUT);
    Serial.begin(115200);
    Serial.println("🚀 Умный горшок с автополивом запущен");
}

void loop() {
    int soilMoisture = analogRead(SOIL_SENSOR_PIN);  // Читаем влажность почвы
    Serial.print("🌱 Влажность почвы: ");
    Serial.println(soilMoisture);

    if (soilMoisture > SOIL_THRESHOLD) {  // Если почва сухая
        Serial.println("💧 Почва сухая! Включаю насос на 1 сек.");
        digitalWrite(RELAY_PIN, HIGH);  // Включаем насос

    } else {
        Serial.println("✅ Почва влажная. Полив не нужен. Выключаю насос");
        digitalWrite(RELAY_PIN, LOW);   // Выключаем насос
    }

    delay(5000);  // Проверяем каждые 5 секунд
}
