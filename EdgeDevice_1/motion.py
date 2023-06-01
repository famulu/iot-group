import random
import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import serial

in_production = False

thingsboard_topic = "v1/devices/me/telemetry"
motion_access_token = "fJGKRSqfLIVyNibrDG1J"
motion_key = "motion"
pot_key = "pot"

motion_topic = "motion"
motion_led_command_topic = "MotionLed"
pot_topic = "pot"

digital_memory = {
    'count': 0,
    'value': None
}

analog_memory = {
    'count': 0,
    'value': None
}

min_reps = 5

def generate_analog_value():
    if analog_memory['count'] == 0 or analog_memory['count'] >= min_reps:
        analog_memory['value'] = random.randrange(0, 1024)
        analog_memory['count'] = 1
    else:
        analog_memory['count'] += 1
        analog_memory['value'] += (random.randrange(0, 51) - 25)

    return analog_memory['value']


def generate_digital_value():
    if digital_memory['count'] == 0 or digital_memory['count'] >= min_reps:
        digital_memory['value'] = random.randrange(0, 2)
        digital_memory['count'] = 1
    else:
        digital_memory['count'] += 1

    return digital_memory['value']


def generate_payload(key, value):
    return "{'" + key + "':" + str(value) + "}"


def publish_value(topic, key, value):
    # Publish to the Mosquitto MQTT broker
    mqtt_client.publish(topic, value, 1)
    print(topic + ": " + str(value))

    # Publish to ThingsBoard
    payload = generate_payload(key, value)
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
            motion_data, pot_data = str(motion_arduino.readline().strip()).split(',')
            publish_value(motion_topic, motion_key, motion_data)
            publish_value(pot_topic, pot_key, pot_data)
else:
    while True:
        motion_data = generate_digital_value()
        pot_data = generate_analog_value()
        publish_value(motion_topic, motion_key, motion_data)
        publish_value(pot_topic, pot_key, pot_data)
        time.sleep(1)

