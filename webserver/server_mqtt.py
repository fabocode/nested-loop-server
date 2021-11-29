import paho.mqtt.client as mqtt
from paho.mqtt.subscribeoptions import SubscribeOptions
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import time
from mqtt_config import MQTTConfig

class MQTTClient:
    def __init__(self, config, client_id, protocol=mqtt.MQTTv5):
        self.config = config
        self.broker_addr = self.config.get_broker_address()
        self.port = self.config.get_port()
        self.username = self.config.get_username()
        self.password = self.config.get_password()
        self.client = mqtt.Client(client_id, protocol=protocol)
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker_addr, self.port)
        self.client.on_message = self.on_message

    def get_pub_properties(self, response_topic, correlation_data):
        publish_properties = Properties(PacketTypes.PUBLISH)
        publish_properties.ResponseTopic = response_topic
        publish_properties.CorrelationData = bytes(correlation_data, 'utf-8')
        return publish_properties
        
    def on_message(self, client, userdata, message):
        try:
            print ("request recieved at server")
            print (message.payload)
            resopnse_topic = message.properties.ResponseTopic
            self.publish(resopnse_topic, 'heroku server message', message.properties)
            print ('response sent from server')
        except:
            print('error')

    def publish(self, topic, payload, properties, qos=0, retain=False):
        self.client.publish(topic, payload, qos, retain=retain, properties=properties)
    
    def subscribe(self, topic, qos=0):
        self.client.subscribe(topic, qos)
    
    def loop(self):
        self.client.loop()
    
    def loop_forever(self):
        self.client.loop_forever()
    
    def loop_start(self):
        self.client.loop_start()
    
    def loop_stop(self):
        self.client.loop_stop()
    
    def disconnect(self):
        self.client.disconnect()
    
    def is_connected(self):
        return self.client.is_connected()
    
if __name__ == "__main__":
    config = MQTTConfig("config/mqtt.yaml")
    client = MQTTClient(config, config.client_name)
    client.subscribe(config.credit_purchased_pub)  # subscribe to response topic for credit purchased

    client.loop_forever()

