import serial
import paho.mqtt.publish as publish
from time import sleep

prev_temp=None
with open('config.json') as json_data_file:
    config = json.load(json_data_file)

def get_temp():
    arduino=serial.Serial("/dev/ttyACM0")
    arduino.baudrate=9600
    data = arduino.readline()
    return data

def publish_message(topic, message):
    print("Publishing to MQTT topic: " + topic)
    print("Message: " + str(message))

    publish.single(topic, str(message), hostname=config["MQTT"]["HOST"],auth={'username':config["MQTT"]["USER"], 'password':config["MQTT"]["PASS"]})

while True:
    if (prev_temp == None):
        prev_temp = float((get_temp().decode("ASCII")).rstrip("\n"))
    else:
        actual_temp = float((get_temp().decode("ASCII")).rstrip("\n"))
        publish_message("SmartHome/sensor", (prev_temp + actual_temp) / 2)
        prev_temp = actual_temp
    sleep(5)



