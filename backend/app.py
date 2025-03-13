# app.py
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

HEADERS =  {
    "Content-Type": "application/json",
    "Authorization": "Token tHmprxyviek19E0HztiulNf8TbfOdAMlGYH8aIcerjP6nGeEB2Wone6U"
}

# Пример эндпоинта /data, который возвращает JSON для фронтенда
@app.route('/data', methods=['GET'])
def get_data():
    # Здесь вы можете вернуть данные датчиков
    # Если у вас нет реальных данных, отдайте тестовые
    fake_data = {
        "temperature": 100,
        "humidity": 100,
        "motion": "Нет движения",
        "smoke": "Не обнаружен",
        "fanThreshold": 100,
        "autoMode": False,
        "led1State": False,
        "led2State": False,
        "fanState": False
    }
    return jsonify(fake_data), 200

@app.route('/api/toggle-led1', methods=['POST'])
def toggle_led1():
    data_switch_lamps = [
        {"topic": "Lamp1", "payload": "1", "retain": False}
    ]
    try:
        response = requests.post(
            "https://dash.wqtt.ru/api/broker/messages/pub",
            headers=HEADERS,
            json=data_switch_lamps
        )
        response.raise_for_status()  # выбросит ошибку, если статус не 200
        # Можно вернуть JSON-ответ от внешнего API
        return jsonify({
            "status": "success",
            "data": response.json()
        }), 200
    except requests.RequestException as e:
        # Логируем или обрабатываем ошибку
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/toggleLED2', methods=['GET'])
def toggle_led2():
    # Логика переключения лампы 2
    return "ВКЛ"

@app.route('/toggleFan', methods=['GET'])
def toggle_fan():
    # Логика переключения вентилятора
    return "ВКЛ"

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
