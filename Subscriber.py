import paho.mqtt.client as mqtt
from Salsa20 import *
import json

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)

    key = "4c3752b70375de25bfbbea8831edb330ee37cc244fc9eb4f03519c2fcb1af4f3"
    nonce = "afc7a6305610b3cf"
    a = Salsa20(key, nonce, len(data["Latitude"]))

    a.salsaDecrypt(data["Latitude"])
    plain1 = a.output
    a.salsaDecrypt(data["Longitude"])
    plain2 = a.output

    data["Latitude"] = plain1
    data["Longitude"] = plain2

    print("\nLatitude :", data["Latitude"])
    print("Longitude :", data["Longitude"])

mqttc = mqtt.Client("subscriber")

mqttc.connect("broker.hivemq.com", 1883)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.subscribe("/raplima/gps",qos=1)

mqttc.loop_forever()
