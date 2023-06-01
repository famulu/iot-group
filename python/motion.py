import random
import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import serial

in_production = False

thingsboard_topic = "v1/devices/me/telemetry"
motion_access_token = "fJGKRSqfLIVyNibrDG1J"
thingsboard_key = "motion"

motion_topic = "motion"
motion_led_command_topic = "MotionLed"


def generate_value():
    return random.randrange(0, 150)


def generate_payload(key, value):
    return "{'" + key + "':" + str(value) + "}"


def publish_value(value):
    mqtt_client.publish(motion_topic, value, 1)
    print(motion_topic + ": " + str(value))

    payload = generate_payload(thingsboard_key, value)
    publish.single(thingsboard_topic, payload, 1, hostname="mqtt.thingsboard.cloud",
                   auth={'username': motion_access_token})
    print(thingsboard_topic + ":" + payload)


def on_connect(client, userdata, flags, rc):
    print("Connected with result: " + mqtt.connack_string(rc))

    client.subscribe(motion_led_command_topic)


def on_message(client, userdata, msg):
    print("Received message: " + msg.payload.decode())
    print("From: " + msg.topic)

    if in_production:
        motion_arduino.write(msg.payload)


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("test.mosquitto.org", 1883, 60)
mqtt_client.loop_start()

if in_production:
    motion_arduino = serial.Serial('/dev/ttyS2', 9600)

    while True:
        if motion_arduino.in_waiting:
            motion_data = motion_arduino.readline().strip()
            publish_value(motion_data)
            print("motion_data: ", motion_data)
else:
    while True:
        publish_value(generate_value())
        time.sleep(1)

