import requests
from test_dt import json_print
headers = {
"Content-Type": "application/json",
"Authorization": "Token tHmprxyviek19E0HztiulNf8TbfOdAMlGYH8aIcerjP6nGeEB2Wone6U"
}
# @json_print
def toggle_led1():
    data_switch_lamps = [
    {"topic": "Lamp1", "payload": "0", "retain": False}
    ]
    return requests.post("https://dash.wqtt.ru/api/broker/messages/pub", headers=headers, json=data_switch_lamps)

toggle_led1()