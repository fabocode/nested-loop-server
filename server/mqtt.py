import paho.mqtt.client as mqtt
from paho.mqtt.subscribeoptions import SubscribeOptions
import time
import os
from urllib.parse import urlparse


def on_message(client, userdata, message):
    try:
        print ("request recieved at server")
        print (message.payload)
        resopnse_topic = message.properties.ResponseTopic
        client.publish(resopnse_topic, 'server message',1, properties=message.properties)
        print ('response sent from server')
    except:
        print('error')


broker_address = 'localhost'

client = mqtt.Client("server", protocol=mqtt.MQTTv5)

url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:18577')
url = urlparse(url_str)
# topic = url.path[1:] or 'test'

# Connect

print(url)
print(f"host: {url.hostname}")
print(f"port: {url.port}")
print(f"username: {url.username}")
print(f"password: {url.password}")
print(f"path: {url.path}")
print("")
client.username_pw_set(url.username, url.password)
client.connect(url.hostname, url.port)

# client.connect(broker_address)

client.subscribe('common', options=SubscribeOptions(noLocal=True))

client.on_message = on_message
print("connected and waiting request")
# client.loop_start()
# time.sleep(10)  # wait
# client.loop_stop()  # stop the loop
client.loop_forever()
client.disconnect()
