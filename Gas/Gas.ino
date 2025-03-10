#include <WiFi.h>
#include <HTTPClient.h>

#define GAS_SENSOR_PIN 32  // Датчик дыма MQ-2 на GPIO32
#define SMOKE_THRESHOLD 900  // Порог тревоги для газа (900-2000)

#define RAIN_SENSOR_PIN 35  // Датчик протечки воды на GPIO35
#define RAIN_THRESHOLD 2500  // Порог тревоги для воды (чем ниже, тем больше воды)

#define TELEGRAM_SEND_DELAY 10000  // Задержка между уведомлениями (10 сек)

const char* ssid = "Tochka";  // Имя Wi-Fi сети
const char* password = "password";  // Пароль Wi-Fi

String botToken = "8031515998:AAHYZ3WZ3h6oTb5WDgFzAoLUEB4ecw8xEfQ"; // API токен Telegram бота
String chatId = "6512586955";  // ID чата в Telegram

unsigned long lastSendTime = 0;  // Переменная для контроля задержки отправки

void sendTelegramMessage(String message) {
    if (millis() - lastSendTime > TELEGRAM_SEND_DELAY) {  // Проверяем задержку
        HTTPClient http;
        String url = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + chatId + "&text=" + message;
        
        http.begin(url);
        int httpCode = http.GET();
        if (httpCode > 0) {
            Serial.println("📩 Сообщение отправлено в Telegram!");
        } else {
            Serial.println("❌ Ошибка отправки!");
        }
        http.end();
        
        lastSendTime = millis();  // Обновляем таймер отправки
    } else {
        Serial.println("⏳ Ждем перед следующей отправкой...");
    }
}

void setup() {
    Serial.begin(115200);
    Serial.println("🚀 Система мониторинга запущена...");

    WiFi.begin(ssid, password);
    Serial.print("🔌 Подключение к Wi-Fi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\n✅ Wi-Fi подключен!");

    sendTelegramMessage("✅ ESP32: Мониторинг газа и протечек запущен!");
}

void loop() {
    // Читаем уровень газа
    int gasValue = analogRead(GAS_SENSOR_PIN);
    Serial.print("🔥 Уровень газа: ");
    Serial.println(gasValue);

    if (gasValue > SMOKE_THRESHOLD) {  
        Serial.println("⚠️ ДЕТЕКЦИЯ ДЫМА! ОПАСНО!");
        sendTelegramMessage("🚨 ОПАСНО! Высокий уровень газа: " + String(gasValue) + " PPM!");
    } else {
        Serial.println("✅ Дым не обнаружен.");
    }

    // Читаем уровень воды (протечки)
    int rainValue = analogRead(RAIN_SENSOR_PIN);
    Serial.print("💦 Уровень воды: ");
    Serial.println(rainValue);

    if (rainValue < RAIN_THRESHOLD) {  
        Serial.println("⚠️ ОБНАРУЖЕНА ПРОТЕЧКА!");
        sendTelegramMessage("🚨 ВНИМАНИЕ! Обнаружена протечка воды! Уровень: " + String(rainValue));
    } else {
        Serial.println("✅ Протечек нет.");
    }

    delay(1000);  // Обновление каждые 1 сек
}
