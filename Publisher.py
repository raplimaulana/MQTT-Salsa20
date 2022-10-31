import paho.mqtt.client as mqtt
import json
import time
from Salsa20 import *
from gps import *

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect")

mqttc = mqtt.Client("publisher")
    
mqttc.on_connect = on_connect
mqttc.connect("broker.hivemq.com", 1883)

while True:
    sensor = gps()

    Latitude = sensor.lat
    Longitude = sensor.lng
    key = "4c3752b70375de25bfbbea8831edb330ee37cc244fc9eb4f03519c2fcb1af4f3"
    nonce = "afc7a6305610b3cf"
    
    a = Salsa20(key,nonce,len(Latitude))
    
    a.salsaEncrypt(Latitude)
    cipher1 = a.output
    a.salsaEncrypt(Longitude)
    cipher2 = a.output
    
    data = {"Latitude": cipher1, "Longitude": cipher2}
    dataJson = json.dumps(data).encode("utf-8")
    
    mqttc.publish("/raplima/gps", payload=dataJson, qos=1)
    
    print("\nPlaintext Latitude\t:", Latitude)
    print("Ciphertext Latitude\t:", cipher1)
    print("\nPlaintext Longitude\t:", Longitude)
    print("Ciphertext Longitude\t:", cipher2)
    
    time.sleep(10)





