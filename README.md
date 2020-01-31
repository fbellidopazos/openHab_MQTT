# Installation
## Install OpenHabian on Raspberry Pi

1. Update & Upgrade System
1. Change password of Sudo(Optional but recommended)
1. Enable SSH(Optional but recommended)
1. Enable Mosquitto Server (Mandatory)
1. Test Accessing http://openhab:8080/

## In OpenHab Paper UI
1.	Install Mqtt Binding(2.X)
1.	Install Amazon Alexa Binding
    1. Register in https://myopenhab.org/login  with UUID and Secret:
        + (Terminal UUID)  ` cat /var/lib/openhab2/uuid && echo`
        + (Terminal Secret)  ` cat /var/lib/openhab2/openhabcloud/secret && echo`
    1. Connect with Amazon echo(Skill=openHab)
    1. Connect with Google Assistant (Skill = openHab)
## SSH/Terminal OpenHabian
### MQTT Broker
1. `sudo nano /etc/openhab2/things/mqtt.things`
```python
Bridge  mqtt:broker:mqtt_broker [
        host="127.0.0.1",
        secure=false,
        port=1883,
        qos=0,
        retain=false,
        clientid="Oh2MqttClient",
        keep_alive_time=30000,
        reconnect_time=60000,
        username="<User>",
        password="<PassWord>"
        ] {
        Thing   topic  mqtt  "MQTT" {
                Channels:
                        Type switch : BoysMain "BoysMain" [
                                commandTopic="SmartHome/Rooms/Boys/Main",
                                stateTopic="SmartHome/Rooms/Boys/Main/state",
                                on="ON",
                                off="OFF"
                                ]
                        Type switch : BoysBath "BoysBath" [
				                                commandTopic="SmartHome/Rooms/Boys/Bathroom", 
				                                stateTopic="SmartHome/Rooms/Boys/Bathroom/state",
                                                on="ON",
                                                off="OFF"
                                                ]
                        Type number : Sensor "Sensor"[
                                                stateTopic="SmartHome/sensor",
                                                unit="ºC"
                                                ]
                        Type rollershutter : Roller "Roller"[
                                                commandTopic="SmartHome/Roller",
                                                stateTopic="SmartHome/Roller/state",
                                                on="ON",
                                                off="OFF",
                                                stop="STOP"
                                                ]
                        Type colorRGB : led "led"[
                                                commandTopic="SmartHome/led",
                                                stateTopic="SmartHome/led/state",
 
                                                ]
                
        }
}
```
To add more 
```
Type <Channel> : <ID> "<Name>" [
                                commandTopic="<Topic>",
                                stateTopic="<Topic/state>",
				                <Channel Parametres>
                                ]

```
Useful Link : Channels and Parametres https://www.openhab.org/addons/bindings/mqtt.generic/

### Items
1. `sudo nano /etc/openhab2/items/home.items`
```python 
Switch BoysMain "My Room" <Light> ["Lighting"]{channel="mqtt:topic:mqtt_broker:mqtt:BoysMain"}
Switch BoysBath "My Bathroom" <Light> ["Lighting"] { channel="mqtt:topic:mqtt_broker:mqtt:BoysBath"}
Number mqtt_sensor "Sensor [%.2f ºC] <Temperature> {channel="mqtt:topic:mqtt_broker:mqtt:Sensor}
Rollershutter Roller "Roller" <rollershutter> ["Switchable"] { channel="mqtt:topic:mqtt_broker:mqtt:Roller"}
Color led "led" <colorlight> [ "Lighting" ] { channel="mqtt:topic:mqtt_broker:mqtt:led"}
```
To add more 
```md
<Type> <id> “<Name>” <Category> [“<AmazonType>”] {channel:” mqtt:topic:mqtt_broker:mqtt:<ID>”}

```
`<ID>` Comes from MQTT Broker channel id

The amazon echo supports the following tags: 
 
1. [ “Switchable” ] This tag is used with the Switch item type, Dimmer item type, Color item type, as well as the Rollershutter item type, but you would not use this for a light that is what the next one is for.
1. [ “Lighting” ] This tag is used for lights with the Switch item type, Dimmer item type, and the Color item type.
1. [ “CurrentTemperature” ] This tag would be used with a device that reports temperature and has the Number item type.
1. [ “Thermostat” ] This tag is used with an item that has a Group item type and has the following devices in the Group
    1. [ “CurrentTemperature” ] or [ “TargetTemperature” ]

Useful Link : Items Types https://www.openhab.org/docs/configuration/items.html#type 

### Sitemap(BasicUI)
1. `sudo nano /etc/openhab2/sitemaps/home.sitemap`
```java
sitemap home label="Smart Home"{
Frame label="My Room"{
	Switch item=BoysMain label="light"
	Switch item=BoysBath label="light"
        Text item=mqtt_sensor label="temperature"
        Switch item=Roller label="rollershutter"
        Colorpicker item=led 
	}
}

```
To add more 
```md
<Type> item=<id> label=”<label>”
```
`<id>` comes from items id
Useful Link : Sitemap Labels https://www.openhab.org/docs/configuration/items.html#type 

## Raspberry Pi (External)
1. Edit config.json accordingly
1. Inset DOC