# app.py
import threading
from mqtt_client import MQTTHandler
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import time
import os
load_dotenv()


MQTT_TOPICS_MONITORING_CONDITION = os.getenv("MQTT_TOPICS_MONITORING_CONDITION", "").replace(" ", "").split(",")

# Название модуля, топики состояния и управления должны называться одинаково (на WQTT)
# Это же название модуля записываем в список переменной "modules"
mqtt_handler = MQTTHandler(
    server=os.getenv("MQTT_SERVER"), port=int(os.getenv("MQTT_PORT")), user=os.getenv("MQTT_USER"),
    password=os.getenv("MQTT_PASSWORD"), topics=MQTT_TOPICS_MONITORING_CONDITION)


# Запускаем MQTT-клиент в отдельном потоке, чтобы он работал параллельно с Flask
mqtt_thread = threading.Thread(target=mqtt_handler.start, daemon=True)
mqtt_thread.start()

app = Flask(__name__)
CORS(app)

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": os.getenv("MQTT_TOKEN_AUTHORIZATION")
}


@app.route('/data', methods=['GET'])
def get_data():
    # Ключ в JSON-ответе соответствует имени топика на MQTT-брокере
    data = {topic: mqtt_handler.sensor_states.get(topic) for topic in MQTT_TOPICS_MONITORING_CONDITION}
    return jsonify(data), 200


@app.route('/api/toggle-module/<module_name>', methods=['POST'])
def toggle_module(module_name):

    """
    Переключает состояние указанного модуля вида true / false.
    """
    if module_name not in mqtt_handler.modules:
        return jsonify({"status": "error", "message": f"Неизвестный модуль: {module_name}"}), 400

    current = mqtt_handler.sensor_states.get(module_name, "0")
    new_state = "true" if current == "false" else "false"
    mqtt_handler.publish(module_name, new_state)
    return jsonify({"status": "success", module_name: new_state}), 200


@app.route('/api/set-light-color', methods=['POST'])
def set_light_color():
    module_name = "toggleRGB"
    data = request.get_json()
    color_from_frontend = data.get('color')  # Получаем цвет в формате HEX

    # Преобразуем HEX в RGB (если нужно)
    if color_from_frontend.startswith('#'):
        color_from_frontend = color_from_frontend.lstrip('#')
        rgb = tuple(int(color_from_frontend[i:i+2], 16) for i in (0, 2, 4))
        color_from_frontend = f"{rgb[0]},{rgb[1]},{rgb[2]}"

    color_from_broker = mqtt_handler.sensor_states.get(module_name, "0")
    if color_from_broker != color_from_frontend:
        mqtt_handler.publish(module_name, color_from_frontend)
        time.sleep(0.1)
        color_from_broker = mqtt_handler.sensor_states.get(module_name, "0")
        if color_from_broker == color_from_frontend:
            return jsonify({"status": "success", "color": color_from_frontend}), 200
        return jsonify(
            {
                "status": "error, no change",
                "message": f"broker: {color_from_broker}, frontend: {color_from_frontend}"
            }), 400
    return jsonify({"status": "Not Modified", "message": "If-Modified-Since"}), 200


@app.route('/api/setFanThreshold/<module_topic>', methods=['POST'])
def threshold_of_modules(module_topic):
    if module_topic not in mqtt_handler.modules:
        return jsonify({"status": "error", "message": f"Неизвестный модуль: {module_topic}"}), 400
    threshold_from_frontend = int(request.get_json().get("threshold"))
    threshold_from_broker = int(mqtt_handler.sensor_states.get(module_topic, "0"))
    if threshold_from_broker != threshold_from_frontend:
        new_state = threshold_from_frontend
        mqtt_handler.publish(module_topic, new_state)
        time.sleep(0.1)
        threshold_from_broker = int(mqtt_handler.sensor_states.get(module_topic, "0"))
        if threshold_from_broker == threshold_from_frontend:
            return jsonify(
                {
                    "status": "success", module_topic: new_state
                }), 200
        return jsonify(
            {
                "status": "error, no changes",
                "message": f"broker:{threshold_from_broker} frontend:{threshold_from_frontend}"
            }), 400
    return jsonify({"status": "Not Modified", "message": f"If-Modified-Since"}), 304


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
