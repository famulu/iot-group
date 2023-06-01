import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

smoke_topic = "smoke"
temp_topic = "temp"
motion_topic = "motion"
pot_topic = "pot"

topic = "v1/devices/me/telemetry"
smoke_access_token = "boPEuDAC9cUgzebtTdTN"
motion_access_token = "24Kb2CAy1UVnFPTFKSJv"
temp_access_token = "E7GODLbhVRwKeeL61WQz"


def generate_payload(key, value):
    return "{'" + key + "':" + str(value) + "}"


def generate_smoke_payload(value):
    return generate_payload("smoke", value)


def generate_temp_payload(value):
    return generate_payload("temp", value)


def generate_motion_payload(value):
    return generate_payload("motion", value)


def generate_pot_payload(value):
    return generate_payload("pot", value)


def publish_value(value, access_token):
    publish.single(topic, value, 1, hostname="172.20.10.6", auth={'username': access_token})


def on_connect(client, userdata, flags, rc):
    print("Connected with result: " + str(rc))

    client.subscribe(smoke_topic)
    client.subscribe(pot_topic)
    client.subscribe(motion_topic)
    client.subscribe(temp_topic)


def on_message(client, userdata, msg):
    if msg.topic == smoke_topic:
        data = msg.payload.decode()
        payload = generate_smoke_payload(data)
        print(payload)
        # publish_value(payload, smoke_access_token)
    if msg.topic == temp_topic:
        data = msg.payload.decode()
        payload = generate_temp_payload(data)
        print(payload)
        # publish_value(payload, temp_access_token)
    if msg.topic == motion_topic:
        data = msg.payload.decode()
        payload = generate_motion_payload(data)
        print(payload)
        # publish_value(payload, motion_access_token)


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("test.mosquitto.org", 1883, 60)

mqtt_client.loop_forever()
