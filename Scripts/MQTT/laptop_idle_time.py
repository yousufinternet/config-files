#!/usr/bin/env python

import time
import socket
import subprocess as sp
import paho.mqtt.client as mqtt
from random import randrange, uniform

username = "homeassistant"
password = sp.check_output(['pass', 'homeserver/homeassistant.mqtt']).strip()
print(password)
mqttBroker = "homeserver"

client = mqtt.Client(f"{socket.gethostname()}_idle_time")
client.username_pw_set(username, password)
client.connect(mqttBroker, port=1883)

while True:
    try:
        idle = int(sp.check_output(['xprintidle']))/1000
    except:
        idle = 'FAIL'
    client.publish('IDLETIME', idle)
    print(f'Published {idle} on IDLETIME')
    time.sleep(10)

