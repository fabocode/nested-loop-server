import paho.mqtt.client as mqtt
import os, json, time 
from urllib.parse import urlparse

credit_purchased = "credit_purchased"
credit_purchased_data = {
    "msg_code": 0x64,
    "data": 40320
}
credit_purchased_res = "credit_purchased_res"


# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload) + " count_publish: " + str(count_publish))
    topic=msg.topic
    if topic == credit_purchased:
        "send an ack?"
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    m_in = json.loads(m_decode)
    print(m_in, topic)

def on_publish(client, obj, mid):
    print(f"published: {mid}")

def on_subscribe(client, obj, mid, granted_qos):
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


# Start subscribe, with QoS level 0
# mqttc.subscribe(credit_purchased, 0)
mqttc.subscribe(credit_purchased, 0)

# Publish a message
# mqttc.publish(topic, "my message")

# Continue the network loop, exit when an error occurs
rc = 0
# while rc == 0:
    # rc = mqttc.loop()
while True:
    rc = mqttc.loop()   # keep network traffic flow with the broker
    # mqttc.publish(topic_serial_number, json.dumps(serial_data))
    mqttc.publish(credit_purchased, json.dumps(credit_purchased_data))
    time.sleep(10)
    print(f"rc: {rc}")
    if rc != 0:
        break
print("rc end: " + str(rc))