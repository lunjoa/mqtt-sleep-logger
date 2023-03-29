#!/usr/bin/python3
import paho.mqtt.client as mqtt
from pyexcel_ods import save_data, get_data
from collections import OrderedDict
import time, json, os

MQTT_SERVER = os.environ.get('MQTT_SERVER')
MQTT_PORT = os.environ.get('MQTT_PORT')
MQTT_PATH = "home-assistant/sleeping"
FILE_NAME = os.environ.get('SLEEPLOGGER_PATH')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    payload = int(msg.payload.decode("utf-8")) == 1
    timestamp = int(time.mktime(time.localtime()))
    print(timestamp)
    print(payload)
    data = get_data(FILE_NAME)
    data['Sheet1'].append([payload,timestamp])
    print(json.dumps(data))
    save_data(FILE_NAME, data)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(os.environ.get('SLEEPLOGGER_USER'), os.environ.get('SLEEPLOGGER_PASSWORD'))
client.connect(MQTT_SERVER, MQTT_PORT, 60)
client.loop_forever()
