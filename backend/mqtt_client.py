import paho.mqtt.client as mqtt


class MQTTHandler:
    def __init__(self, server, port, user, password, topics: dict[str:str]):
        self.server = server
        self.port = port
        self.modules = topics
        # Инициализируем состояния для каждого модуля (по умолчанию "0" — выключено)
        self.sensor_states = {module: "0" for module in topics}

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

