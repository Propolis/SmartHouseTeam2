# app.py

import threading
from mqtt_client import MQTTHandler
from flask import Flask, jsonify, request
from flask_cors import CORS
import time


TOPICS = ["RGBLenta_Bedroom", "Water", "powerVentilation", "toggleRGB", "Protechka"]

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
        "State_of_Lamp_Bathroom": mqtt_handler.sensor_states.get("Lamp_Bathroom"),
        "State_of_Ventilation": mqtt_handler.sensor_states.get("powerVentilation"),
        "State_of_Water": mqtt_handler.sensor_states.get("Water"),
        "toggleRGB": mqtt_handler.sensor_states.get("toggleRGB"),
        "Protechka": mqtt_handler.sensor_states.get("Protechka"),
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
    mqtt_handler.publish(module_name, color_from_frontend)
    time.sleep(0.1)
    color_from_broker = mqtt_handler.sensor_states.get(module_name, "0")
    if color_from_broker == color_from_frontend:
        return jsonify({"status": "success", "color": data}), 200
    return jsonify({"status": "error", "message": f"broker:{color_from_broker} \n frontend: {color_from_frontend}"}), 400



@app.route('/setFanThreshold', methods=['GET'])
def set_fan_threshold():
    threshold = request.args.get('threshold', '30')
    # Логика сохранения порога вентилятора
    return f"Порог установлен на {threshold}"

@app.route('/toggleAutoMode', methods=['GET'])
def toggle_auto_mode():
    # Логика переключения авто/ручного режима
    return "Режим переключен"

if __name__ == '__main__':
    app.run(debug=True, port=3001)
