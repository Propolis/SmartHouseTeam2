import paho.mqtt.client as mqtt
import time

# Настройки
MQTT_SERVER = "m1.wqtt.ru"
MQTT_PORT = 13010             # порт без TLS
MQTT_USER = "u_TNQXY5"        # ваш логин
MQTT_PASSWORD = "6En7SeKP"    # ваш пароль
TOPIC_SUB = "Lamp1"  # топик для подписки
TOPICS_STATE = ["StateLamp1", "StateLamp2"]

def on_connect(client, userdata, flags, reasonCode):
    if reasonCode == 0:
        print("MQTTv5: Подключились успешно")
        # client.subscribe(TOPICS_STATE[0])
        client.subscribe("StateLamp2")
        # map(client.subscribe, TOPICS_STATE)
    else:
        print("Ошибка подключения:", reasonCode)

def on_message(client, userdata, msg):
    payload_str = msg.payload.decode('utf-8')
    print(f"Получено сообщение из {msg.topic}: {payload_str}")

# Создаем MQTT-клиент
client = mqtt.Client(protocol=mqtt.MQTTv311)

client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Назначаем обработчики
client.on_connect = on_connect
client.on_message = on_message

# Подключаемся к брокеру
client.connect(MQTT_SERVER, MQTT_PORT, keepalive=60)

# Запускаем цикл обработки сообщений (блокирующе)
client.loop_forever()
