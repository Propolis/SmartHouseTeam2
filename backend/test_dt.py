import requests
from json import dumps

# Декоратор для красивого вывода JSON
def json_print(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)  # Вызываем переданную функцию
        try:
            print(dumps(response.json(), indent=4, ensure_ascii=False))
        except requests.exceptions.JSONDecodeError:
            print("Ошибка декодирования JSON:", response.text)
    return wrapper  # Возвращаем обёрнутую функцию

# Заголовки запроса с авторизацией
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token tHmprxyviek19E0HztiulNf8TbfOdAMlGYH8aIcerjP6nGeEB2Wone6U"
}

# 1. Получение списка всех устройств
@json_print
def list_all_devices():
    return requests.get("https://dash.wqtt.ru/api/devices", headers=headers)

# 2. Получение информации об устройстве по ID
@json_print
def get_device_by_id(device_id):
    return requests.get(f"https://dash.wqtt.ru/api/devices/{device_id}", headers=headers)

# 3. Переключение ламп
@json_print
def switch_lamps():
    data_switch_lamps = [
        # {"topic": "Lamp1", "payload": "1", "retain": False},
        {"topic": "Lamp2", "payload": "1", "retain": False}
    ]
    return requests.post("https://dash.wqtt.ru/api/broker/messages/pub", headers=headers, json=data_switch_lamps)


@json_print
def check_condition():
    data_switch_lamps = [
        {"topic": "StateLamp1"},
    ]
    return requests.post("https://dash.wqtt.ru/api/broker/messages/pub", headers=headers, json=data_switch_lamps)



def main():
    # Вызовы функций
    # list_all_devices()  # Выведет список устройств
    # get_device_by_id(50882)  # Выведет данные об устройстве с ID 50882
    switch_lamps()  # Отправит команду на включение/выключение ламп
    # check_condition()
    # pass


if __name__ == "__main__":
    main()
