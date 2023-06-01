import random
import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import serial

in_production = False

thingsboard_topic = "v1/devices/me/telemetry"
smoke_access_token = "l5rnGguS4Yje8axG8wGb"
thingsboard_key = "smoke"

smoke_topic = "smoke"

buzzer_command_topic = "SmokeBuzzer"
smoke_led_command_topic = "SmokeLed"


def generate_value():
    return random.randrange(40, 200)


def generate_payload(key, value):
    return "{'" + key + "':" + str(value) + "}"


def publish_value(value):
    mqtt_client.publish(smoke_topic, value, 1)
    print(smoke_topic + ": " + str(value))

    payload = generate_payload(thingsboard_key, value)
    publish.single(thingsboard_topic, payload, 1, hostname="mqtt.thingsboard.cloud",
                   auth={'username': smoke_access_token})
    print(thingsboard_topic + ":" + payload)


def on_connect(client, userdata, flags, rc):
    print("Connected with result: " + mqtt.connack_string(rc))

    client.subscribe(buzzer_command_topic)
    client.subscribe(smoke_led_command_topic)


def on_message(client, userdata, msg):
    print("Received message: " + msg.payload.decode())
    print("From: " + msg.topic)

    if in_production:
        smoke_arduino.write(msg.payload)


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("test.mosquitto.org", 1883, 60)
mqtt_client.loop_start()

if in_production:
    smoke_arduino = serial.Serial('/dev/ttyS1', 9600)

    while True:
        if smoke_arduino.in_waiting:
            smoke_data = smoke_arduino.readline().strip()
            publish_value(smoke_data)
else:
    while True:
        publish_value(generate_value())
        time.sleep(2)
