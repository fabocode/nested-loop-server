import paho.mqtt.client as mqtt
from paho.mqtt.subscribeoptions import SubscribeOptions
import time


def on_message(client, userdata, message):
    try:
        print ("request recieved at server")
        print (message.payload)
        resopnse_topic = message.properties.ResponseTopic
        client.publish(resopnse_topic, 'server message',1, properties=message.properties)
        print ('response sent from server')
    except:
        print('error')


# broker_address = 'localhost'
broker_address = 'mqtt.flespi.io'
port = 1883 
username = "n9WOlAdDGxS4DMdKBSOyLla0JYIIIdQWcCym1APxXvqq5rZw9DTINRymF5Tb8zX9"
password = ""

client = mqtt.Client("server", protocol=mqtt.MQTTv5)
client.username_pw_set(username, password)
client.connect(broker_address, port)

client.subscribe("hev/credit_purchased/publish", options=SubscribeOptions(noLocal=True))
# client.subscribe('common', options=SubscribeOptions(noLocal=True))

client.on_message = on_message
# client.loop_start()
# time.sleep(10)  # wait
# client.loop_stop()  # stop the loop
client.loop_forever()
