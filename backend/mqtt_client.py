# mqtt_client.py
import paho.mqtt.client as mqtt

# Глобальная переменная, где будем хранить последнее состояние лампы
lamp1_state = None

# Настройки MQTT (пример, адаптируйте под свои данные)
MQTT_SERVER = "m1.wqtt.ru"
MQTT_PORT = 13010
MQTT_USER = "u_TNQXY5"
MQTT_PASSWORD = "6En7SeKP"
TOPICS_STATE = ["StateLamp1", "StateLamp2"]
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT: Подключились успешно")
        # Подписываемся на топик состояния
        map(client.subscribe, TOPICS_STATE)
    else:
        print(f"MQTT: Ошибка подключения. Код: {rc}")

def on_message(client, userdata, msg):
    global lamp1_state
    payload_str = msg.payload.decode('utf-8')
    print(f"MQTT: Получено сообщение из {msg.topic}: {payload_str}")
    lamp1_state = payload_str  # Сохраняем последнее полученное состояние

def create_mqtt_client():
    """Создаёт и настраивает MQTT-клиент, готовый к подключению."""
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    return client
