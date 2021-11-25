import paho.mqtt.client as mqtt
import os
from urllib.parse import urlparse

count_publish = 0 

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    global count_publish
    count_publish += 1
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload) + " count_publish: " + str(count_publish))

def on_publish(client, obj, mid):
    print(f"published: {count_publish}")

def on_subscribe(client, obj, mid, granted_qos):
    global count_publish
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

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
mqttc.username_pw_set(url.username, url.password)
mqttc.connect(url.hostname, url.port)


topic_credit_purchased = "credit_purchased"
# Start subscribe, with QoS level 0
mqttc.subscribe(topic_credit_purchased, 0)

# Publish a message
# mqttc.publish(topic, "my message")

# Continue the network loop, exit when an error occurs
# rc = 0
# while rc == 0:
#     rc = mqttc.loop()
mqttc.loop_forever()
print("rc: " + str(rc))
