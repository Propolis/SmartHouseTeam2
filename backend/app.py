# app.py

import threading
from mqtt_client import MQTTHandler
from flask import Flask, jsonify, request
from flask_cors import CORS
import time


TOPICS = ["RGBLenta_Bedroom", "Klimat_Kontrol", "powerVentilation",
          "toggleRGB", "Protechka", "VentilationVlaznost", "VlaznostPorog",
          "ModeVentilation", "Pompa", "Rezimi_Klimat_Kontrol", "TemperaturePorog"

          ]

# Название модуля, топики состояния и управления должны называться одинаково (на WQTT)
# Это же название модуля записываем в список переменной "modules"
mqtt_handler = MQTTHandler(server="m1.wqtt.ru", port=13010, user="u_TNQXY5", password="6En7SeKP",
                           topics=TOPICS)



# Запускаем MQTT-клиент в отдельном потоке, чтобы он работал параллельно с Flask
mqtt_thread = threading.Thread(target=mqtt_handler.start, daemon=True)
mqtt_thread.start()

app = Flask(__name__)
CORS(app)

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Token tHmprxyviek19E0HztiulNf8TbfOdAMlGYH8aIcerjP6nGeEB2Wone6U"
}

# Пример эндпоинта /data, который возвращает JSON для фронтенда
@app.route('/data', methods=['GET'])
def get_data():

    data = {
        "temperature": 19,
        "humidity": 64,
        "motion": "Нет движения",
        "smoke": "Не обнаружен",
        "fanThreshold": 20,
        "autoMode": 1,
        "State_of_Lamp_Bedroom": mqtt_handler.sensor_states.get("RGBLenta_Bedroom"),
        "State_of_Ventilation": mqtt_handler.sensor_states.get("powerVentilation"),
        "State_of_Klimat_Kontrol": mqtt_handler.sensor_states.get("Klimat_Kontrol"),
        "toggleRGB": mqtt_handler.sensor_states.get("toggleRGB"),
        "Protechka": mqtt_handler.sensor_states.get("Protechka"),
        "Humidity_bathroom": mqtt_handler.sensor_states.get("VentilationVlaznost"),
        "VlaznostPorog": mqtt_handler.sensor_states.get("VlaznostPorog"),
        "ModeVentilation": mqtt_handler.sensor_states.get("ModeVentilation"),
        "Rezimi_Klimat_Kontrol": mqtt_handler.sensor_states.get("Rezimi_Klimat_Kontrol"),
        "Pompa": mqtt_handler.sensor_states.get("Pompa"),
        "TemperaturePorog": mqtt_handler.sensor_states.get("TemperaturePorog"),
    }

    return jsonify(data), 200


@app.route('/api/toggle-module/<module_name>', methods=['POST'])
def toggle_module(module_name):

    """
    Переключает состояние указанного модуля вида 0 / 1.
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
    color_from_frontend = f"{data.get('red')},{data.get('green')},{data.get('blue')}"
    color_from_broker = mqtt_handler.sensor_states.get(module_name, "0")
    if color_from_broker != color_from_frontend:
        mqtt_handler.publish(module_name, color_from_frontend)
        time.sleep(0.1)
        color_from_broker = mqtt_handler.sensor_states.get(module_name, "0")
        if color_from_broker == color_from_frontend:
            return jsonify({"status": "success", "color": data}), 200
        return jsonify({"status": "error,no change", "message": f"broker:{color_from_broker} \n frontend: {color_from_frontend}"}), 400
    return jsonify({"status": "Not Modified", "message": f"If-Modified-Since"}), 304


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
            return jsonify({"status": "success", module_topic: new_state}), 200
        return jsonify(
            {"status": "error, no changes", "message": f"broker:{threshold_from_broker} frontend:{threshold_from_frontend}"}), 400
    return jsonify({"status": "Not Modified", "message": f"If-Modified-Since"}), 304
@app.route('/toggleAutoMode', methods=['GET'])
def toggle_auto_mode():
    # Логика переключения авто/ручного режима
    return "Режим переключен"

if __name__ == '__main__':
    app.run(debug=True, port=3001)
