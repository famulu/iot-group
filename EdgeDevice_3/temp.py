import random
import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import serial

in_production = False

thingsboard_topic = "v1/devices/me/telemetry"
temp_access_token = "9KDPDLVh804BkGWxj4Ht"
thingsboard_key = "temp"

temp_topic = "temp"
fan_command_topic = "ThermoFan"
thermo_led_command_topic = "ThermoLed"


def generate_value():
    return random.randrange(23, 28)


def generate_payload(key, value):
    return "{'" + key + "':" + str(value) + "}"


def publish_temp_value(value):
    mqtt_client.publish(temp_topic, value, 1)
    print(temp_topic + ": " + str(value))

    payload = generate_payload(thingsboard_key, value)
    publish.single(thingsboard_topic, payload, 1, hostname="mqtt.thingsboard.cloud",
                   auth={'username': temp_access_token})
    print(thingsboard_topic + ":" + payload)


def on_connect(client, userdata, flags, rc):
    print("Connected with result: " + mqtt.connack_string(rc))

    client.subscribe(fan_command_topic)
    client.subscribe(thermo_led_command_topic)


def on_message(client, userdata, msg):
    print("Received message: " + msg.payload.decode())
    print("From: " + msg.topic)

    if in_production:
        temp_arduino.write(msg.payload)


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("test.mosquitto.org")
mqtt_client.loop_start()

if in_production:
    temp_arduino = serial.Serial('/dev/ttyS0', 9600)

    while True:
        if temp_arduino.in_waiting:
            temp_data = temp_arduino.readline().strip()
            publish_temp_value(temp_data)
            print("temp_data: ", temp_data)
else:
    while True:
        publish_temp_value(generate_value())
        time.sleep(2)
