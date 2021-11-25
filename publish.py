import paho.mqtt.client as mqtt
import os
from urllib.parse import urlparse
import time

count_publish = 0 

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(client, obj, mid):
    global count_publish
    count_publish += 1
    print(f"published: {count_publish}")

def on_subscribe(client, obj, mid, granted_qos):
    global count_publish
    print("Subscribed: " + str(mid) + " " + str(granted_qos) + " count_publish: " + str(count_publish))

def on_log(client, obj, level, string):
    print(string)

mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
# mqttc.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:18577')
url = urlparse(url_str)
topic = url.path[1:] or 'test'

# Connect
print(f"url {url} - topic: {topic}")
print(f"username: {url.username} - password: {url.password}")
print(f"hostname: {url.hostname} - port: {url.port}")
print(f"path: {url.path}")
print("")
mqttc.username_pw_set(url.username, url.password)
mqttc.connect(url.hostname, url.port)

# Start subscribe, with QoS level 0
# mqttc.subscribe(topic, 0)

# Publish a message
mqttc.publish(topic, "my message from pc")

# Continue the network loop, exit when an error occurs
rc = 0
# while rc == 0:
    # rc = mqttc.loop()
while True:
    rc = mqttc.loop()   # keep network traffic flow with the broker
    mqttc.publish(topic, "my message from pc")
    time.sleep(10)
    print(f"rc: {rc}")
    if rc != 0:
        break
print("rc end: " + str(rc))
