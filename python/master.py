import random
import time

import paho.mqtt.client as mqtt
import serial

in_development = True

thingsboard_topic = "v1/devices/me/telemetry"
smoke_access_token = "boPEuDAC9cUgzebtTdTN"
motion_access_token = "24Kb2CAy1UVnFPTFKSJv"
temp_access_token = "E7GODLbhVRwKeeL61WQz"

smoke_topic = "smoke"
motion_topic = "motion"
temp_topic = "temp"
pot_topic = "pot"

buzzer_command_topic = "SmokeBuzzer"
fan_command_topic = "ThermoFan"
thermo_led_command_topic = "ThermoLed"
smoke_led_command_topic = "SmokeLed"
motion_led_command_topic = "MotionLed"

def generate_value():
    return random.randrange(1024)


def publish_smoke_value(value):
    publish_value(value, smoke_topic)


def publish_motion_value(value):
    publish_value(value, motion_topic)


def publish_temp_value(value):
    publish_value(value, temp_topic)


def publish_pot_value(value):
    publish_value(value, pot_topic)


def publish_value(value, topic: str):
    client.publish(topic, value, 1)
    print(topic + ": " + str(value))


def on_connect(client, userdata, flags, rc):
    print("Connected with result: " + mqtt.connack_string(rc))

    client.subscribe(buzzer_command_topic)
    client.subscribe(fan_command_topic)
    client.subscribe(thermo_led_command_topic)
    client.subscribe(smoke_led_command_topic)
    client.subscribe(motion_led_command_topic)


def on_message(client, userdata, msg):
    print("Received message: " + msg.payload.decode())
    print("From: " + msg.topic)

    if msg.topic == buzzer_command_topic or msg.topic == smoke_led_command_topic:
        smoke_arduino.write(msg.payload)
    if msg.topic == fan_command_topic or msg.topic == thermo_led_command_topic:
        temp_arduino.write(msg.payload)
    if msg.topic == motion_led_command_topic:
        motion_arduino.write(msg.payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)
client.loop_start()

if not in_development:
    smoke_arduino = serial.Serial('/dev/ttyS1', 9600)
    temp_arduino = serial.Serial('/dev/ttyS0', 9600)
    motion_arduino = serial.Serial('/dev/ttyS2', 9600)

    while True:
        if temp_arduino.in_waiting:
            temp_data = temp_arduino.readline().strip()
            publish_temp_value(temp_data)
            print("temp_data: ", temp_data)

        if motion_arduino.in_waiting:
            motion_data = motion_arduino.readline().strip()
            publish_motion_value(motion_data)
            print("motion_data: ", motion_data)

        if smoke_arduino.in_waiting:
            smoke_data = smoke_arduino.readline().strip()
            publish_smoke_value(smoke_data)
            print("motion_data: ", smoke_data)
else:
    while True:
        publish_smoke_value(generate_value())
        publish_pot_value(generate_value())
        publish_temp_value(generate_value())
        publish_motion_value(generate_value())

        time.sleep(1)
