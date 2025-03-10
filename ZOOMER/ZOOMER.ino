const int buzzerPin = 23; // GPIO, к которому подключён зуммер

void setup() {
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  tone(buzzerPin, 1000); // Генерация звука частотой 1000 Гц
  delay(1000);           // Звук 1 секунда
  noTone(buzzerPin);     // Остановить звук
  delay(1000);           // Пауза 1 секунда
}
