import paho.mqtt.client as mqtt

a = {
    'module': {
        'topic1': 0,
        'topic2': 0,
        'topic3': 0,
    }
}
class MQTTHandler:
    def __init__(self, server, port, user, password, modules: dict[str:str]):
        self.server = server
        self.port = port
        self.modules = modules
        # Инициализируем состояния для каждого модуля (по умолчанию "0" — выключено)
        self.sensor_states = {module: "0" for module in modules}

        # Создаем MQTT-клиент с новой версией API
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv311)
        self.client.username_pw_set(user, password)

        # Назначаем обработчики
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("✅ MQTT: Подключились успешно")
            for topic in self.modules:
                client.subscribe(topic)
                print(f"📡 Подписались на {topic}")
        else:
            print(f"❌ Ошибка подключения: {rc}")

    def on_message(self, client, userdata, msg, properties=None):
        payload_str = msg.payload.decode('utf-8')
        print(f"📥 Получено сообщение из {msg.topic}: {payload_str}")
        # Обновляем состояние для топика
        self.sensor_states[msg.topic] = payload_str
        print(self.sensor_states)

    def start(self):
        """Запускает MQTT-клиент в фоновом режиме (не блокирует выполнение)."""
        self.client.connect(self.server, self.port, keepalive=60)
        self.client.loop_start()  # Фоновый цикл обработки сообщений

    def publish(self, topic, payload):
        """Отправляет сообщение в указанный топик."""
        self.client.publish(topic, payload)
        print(f"📤 Отправлена команда: {payload} в {topic}")


# Пример использования (тестовый запуск)
if __name__ == "__main__":
    # Задаем параметры подключения и список топиков (модулей)
    mqtt_handler = MQTTHandler(
        server="m1.wqtt.ru",
        port=13010,
        user="u_TNQXY5",
        password="6En7SeKP",
        modules=["Lamp1", "Lamp2"]
    )

    # Запускаем MQTT-клиент в фоновом режиме
    mqtt_handler.start()

    # Немного подождем, чтобы клиент успел подключиться и подписаться
    import time

    # Оставляем приложение запущенным
    while True:
        time.sleep(1)
