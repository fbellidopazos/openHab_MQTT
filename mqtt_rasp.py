# Import package
import json
import paho.mqtt.client as mqtt
#add for output
import RPi.GPIO as GPIO
import socket

with open('config.json') as json_data_file:
    config = json.load(json_data_file)

MQTT_HOST = config["MQTT"]["HOST"]
MQTT_PORT = config["MQTT"]["PORT"]
MQTT_KEEPALIVE_INTERVAL = config["MQTT"]["KEEPALIVE_INTERVAL"]
MQTT_TOPIC = config["MQTT"]["TOPICS"]

LEDS=config["LEDS"]
for i in LEDS:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(i, GPIO.OUT)

try:
    def on_connect(self, mosq, obj, rc):
        for i in MQTT_TOPIC:
            mqttc.subscribe(i, 0)
            print("Connect on " + MQTT_HOST)
            mqttc.publish(i + "/alive", "alive")
            mqttc.publish(i + "/IP", get_ip())
            mqttc.publish(i + "/name", "MQTT_RASP")

    def on_subscribe(mosq, obj, mid, granted_qos):
        print("Subscribed to <Topic> with QoS: " + str(granted_qos))


    def on_message(mosq, obj, msg):
        for i in range(0,len(MQTT_TOPIC)):
            if(str(msg.topic) == MQTT_TOPIC[i]):
                if (msg.payload == 'ON'):
                    GPIO.output(LEDS[i], True)
                    print("Topic: " + str(msg.topic))
                    print("QoS: " + str(msg.qos))
                    print(str(LEDS[i])+"is ON")
                    mqttc.publish(MQTT_TOPIC[i] + "/state", "ON")
                if (msg.payload == 'OFF'):
                    GPIO.output(LEDS[i], False)
                    print("Topic: " + str(msg.topic))
                    print("QoS: " + str(msg.qos))
                    print(str(LEDS[i]) + "is OFF")
                    mqttc.publish(MQTT_TOPIC[i] + "/state", "OFF")
                break

    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    print(get_ip())
    # Initiate MQTT Client
    mqttc = mqtt.Client()
    mqttc.username_pw_set(config["MQTT"]["USER"],config["MQTT"]["PASS"])
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe

    # Connect with MQTT Broker
    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

    # Continue monitoring the incoming messages for subscribed topic
    mqttc.loop_forever()
except KeyboardInterrupt:
    # here you put any code you want to run before the program
    # exits when you press CTRL+C
    for i in MQTT_TOPIC:
        mqttc.publish(i+"/state","OFF")
    GPIO.cleanup()
