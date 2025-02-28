// Пины, к которым подключены датчики MQ-2
const int sensorPins[] = {12, 27, 25, 32};  // GPIO пины
const int numSensors = sizeof(sensorPins) / sizeof(sensorPins[0]); // Количество датчиков

void setup() {
    Serial.begin(115200);  // Запускаем монитор порта
    delay(1000);  // Даем ESP32 запуститься
    Serial.println("Старт считывания MQ-2 датчиков...");
}

void loop() {
    Serial.println("-------------");
    for (int i = 0; i < numSensors; i++) {
        int sensorValue = analogRead(sensorPins[i]);  // Считываем аналоговое значение
        Serial.print("Датчик #");
        Serial.print(i + 1);
        Serial.print(" (GPIO ");
        Serial.print(sensorPins[i]);
        Serial.print("): ");
        Serial.println(sensorValue);
    }
    Serial.println("-------------");
    delay(2000);  // Пауза между измерениями
}
