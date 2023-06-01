from flask import Flask, render_template, url_for, redirect, request
import paho.mqtt.publish as publish


def publish_value(value: int, topic: str):
    print(topic + ":" + str(value))
    publish.single(topic, value, 1, hostname="test.mosquitto.org")


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# System 1 Thermostat
@app.route('/startS1Fan')
def startS1Fan():
    publish_value(3, "ThermoFan")
    return redirect(url_for('index'))


@app.route('/stopS1Fan')
def stopS1Fan():
    publish_value(4, "ThermoFan")
    return redirect(url_for('index'))


@app.route('/startS1Led')
def startS1Led():
    publish_value(1, "ThermoLed")
    return redirect(url_for('index'))


@app.route('/stopS1Led')
def stopS1Led():
    publish_value(2, "ThermoLed")
    return redirect(url_for('index'))


# System 2 Smoke detection
@app.route('/startS2Buzzer')
def startS2Buzzer():
    publish_value(3, "SmokeBuzzer")
    return redirect(url_for('index'))


@app.route('/stopS2Buzzer')
def stopS2Buzzer():
    publish_value(4, "SmokeBuzzer")
    return redirect(url_for('index'))


@app.route('/startS2Led')
def startS2Led():
    publish_value(1, "SmokeLed")
    return redirect(url_for('index'))


@app.route('/stopS2Led')
def stopS2Led():
    publish_value(2, "SmokeLed")
    return redirect(url_for('index'))


# System 3 Motion activatied light system
@app.route('/startS3')
def startS3():
    publish_value(1, "MotionLed")
    return redirect(url_for('index'))


@app.route('/stopS3')
def stopS3():
    publish_value(2, "MotionLed")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
