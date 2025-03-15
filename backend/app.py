# app.py
from flask import Flask, jsonify, request
import requests
import threading
from mqtt_client import MQTTHandler
from flask import Flask, jsonify, request
from flask_cors import CORS





# Название модуля, топики состояния и управления должны называться одинаково (на WQTT)
# Это же название модуля записываем в список переменной "modules"
mqtt_handler = MQTTHandler(
    server="m1.wqtt.ru",
    port=13010,
    user="u_TNQXY5",
    password="6En7SeKP",
    modules=["Lamp_Bedroom", "Lamp_Bathroom", "Water", "Ventilation"]
)



# Запускаем MQTT-клиент в отдельном потоке, чтобы он работал параллельно с Flask
mqtt_thread = threading.Thread(target=mqtt_handler.start, daemon=True)
mqtt_thread.start()

app = Flask(__name__)
CORS(app)

HEADERS =  {
    "Content-Type": "application/json",
    "Authorization": "Token tHmprxyviek19E0HztiulNf8TbfOdAMlGYH8aIcerjP6nGeEB2Wone6U"
}

# Пример эндпоинта /data, который возвращает JSON для фронтенда
@app.route('/data', methods=['GET'])
def get_data():

    data = {
        "data": {
            "temperature": 100,
            "humidity": 100,
            "motion": "Нет движения",
            "smoke": "Не обнаружен",
            "fanThreshold": 100,
            "autoMode": False,
            "State_of_Lamp_Bedroom": mqtt_handler.sensor_states.get("Lamp_Bedroom"),
            "State_of_Lamp_Bathroom": mqtt_handler.sensor_states.get("Lamp_Bathroom"),
            "State_of_Ventilation": mqtt_handler.sensor_states.get("Ventilation"),
            "State_of_Water": mqtt_handler.sensor_states.get("Water"),
        }
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
    new_state = "1" if current == "0" else "0"
    mqtt_handler.publish(module_name, new_state)
    return jsonify({"status": "success", module_name: new_state}), 200


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
