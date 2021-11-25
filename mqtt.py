#!C:/python36/python.exe
#!/usr/bin/env python3
##demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
##Free to use for any purpose
##If you like and use this code you can
##buy me a drink here https://www.paypal.me/StepenCope

import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes 
import time,logging,sys, os
from urllib.parse import urlparse

client_id="testclient2"
mqttv=mqtt.MQTTv5
messages=[]
host = '192.168.1.41'
port=1883
pub_topic="test"

def on_publish(client, userdata, mid):
    print("published")

def on_connect(client, userdata, flags, reasonCode,properties=None):
    print('Connected ',flags)
    print('Connected properties',properties)
    print('Connected ',reasonCode)



def on_message(client, userdata, message):

    msg=str(message.payload.decode("utf-8"))
    messages.append(msg)
    print('RECV Topic = ',message.topic)
    print('RECV MSG =', msg)
    response_topic = message.properties.ResponseTopic
    properties=Properties(PacketTypes.PUBLISH)
    properties.CorrelationData=message.properties.CorrelationData
    print('Responding on response topic:', properties)
    #respond
    
    client.publish(response_topic,"server response message",properties=properties)


def on_disconnect(client, userdata, rc):
    print('Received Disconnect ',rc)

def on_subscribe(client, userdata, mid, granted_qos,properties=None):
    print('SUBSCRIBED')

def on_unsubscribe(client, userdata, mid, properties, reasonCodes):
    print('UNSUBSCRIBED') 
    



print("creating client")

client = mqtt.Client("server",protocol=mqttv)


client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_publish = on_publish

properties=None

# Parse CLOUDMQTT_URL (or fallback to localhost)
url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:18577')
url = urlparse(url_str)
topic = url.path[1:] or 'test'

# Connect
client.username_pw_set(url.username, url.password)
client.connect(host,port,properties=properties)

time.sleep(5)
client.subscribe('org/common')
time.sleep(2)

print("Publish response topic")
msg_out1="test message from client 1"
properties=Properties(PacketTypes.PUBLISH)
properties.ResponseTopic='org/responses/server'
#client.publish('org/common',"test Message",properties=properties)

client.loop_forever()




