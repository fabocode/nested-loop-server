import paho.mqtt.client as mqtt
import os, json, time 
from urllib.parse import urlparse
from mqtt_conf import MQTT_Config


mqtt_data = MQTT_Config()


# Client ID 
client_id = "HEV123"
# Server/backend/broker ID
server_id = "SERVER321"

###########################################################
# Notifications 
# message: credit purchased
# source: server 
# publish 
credit_purchased_server_tx = "credit_purchased_srvr_tx"
credit_purchased_data_tx = {
    "msg_code": 0x64,
    "data": 40320
}
# subscribe topic to receive ACK
credit_purchased_hev_rx = "credit_purchased_hev_rx"

# message: serial number 
# source: hev 
# publish 
serial_number_hev_tx = "serial_number_hev_tx"
serial_number_data_tx = {
    "msg_code": 0x65,
    "data": "ACK"
}
# subscribe topic to receive ACK
serial_number_server_rx = "serial_number_server_rx"

# message: technician request
# source: hev 
# subscriber: server
# Posible options:
    # SSR_FAULT
    # DC_AC_FAULT
# Response: ACK
technician_request_hev_tx = "technician_request_hev_tx"
technician_request_data_tx = {
    "msg_code": 0x66,
    "data": {
        "reason": "ACK"
    }
}
# publish to mqtt
technician_request_server_rx = "technician_request_server_rx"

# message: thermical shutdown 
# source: hev 
# subscriber: server
# Posible options:
    # SSR_FAULT
    # DC_AC_FAULT
# Response: ACK
thermical_shutdown_hev_tx = "thermical_shutdown_hev_tx"
thermical_shutdown_data_tx = {
    "msg_code": 0x67,
    "data": "ACK",
}
# publish to mqtt
thermical_shutdown_server_rx = "thermical_shutdown_server_rx"

# message: alert level
# source: hev
# subscriber: server
alert_level_hev_tx = "alert_level_hev_tx"
alert_level_data_tx = {
    "msg_code": 0x68,
    "data": "ACK"
}
# publish to mqtt
alert_level_server_rx = "alert_level_server_rx"


# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    topic=msg.topic
    if topic == credit_purchased_hev_rx:
        # ACK received from HEV
        print(f"topic: {msg.topic}, payload: {msg.payload}")

    elif topic == serial_number_hev_tx:
        print(f"topic: {msg.topic}, payload: {msg.payload}")
        # save data from serial number 
        # send ACK to HEV
        mqttc.publish(serial_number_server_rx, json.dumps(serial_number_data_tx))
        # m_decode=str(msg.payload.decode("utf-8","ignore"))
        # m_in = json.loads(m_decode)
        # print(m_in, topic)
        # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    elif topic == technician_request_hev_tx:
        print(f"topic: {msg.topic}, payload: {msg.payload}")
        # save data from technician request
        # send ACK to HEV
        mqttc.publish(technician_request_server_rx, json.dumps(technician_request_data_tx))
    
    elif topic == thermical_shutdown_hev_tx:
        print(f"topic: {msg.topic}, payload: {msg.payload}")
        # save data from technician request
        # send ACK to HEV
        mqttc.publish(thermical_shutdown_server_rx, json.dumps(thermical_shutdown_data_tx))

    elif topic == alert_level_hev_tx:
        print(f"topic: {msg.topic}, payload: {msg.payload}")
        # save data from technician request
        # send ACK to HEV
        mqttc.publish(alert_level_server_rx, json.dumps(alert_level_data_tx))

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
mqttc.subscribe(credit_purchased_hev_rx, 0)
mqttc.subscribe(serial_number_hev_tx, 0)
mqttc.subscribe(technician_request_hev_tx, 0)
mqttc.subscribe(credit_purchased_server_tx, 0)
mqttc.subscribe(thermical_shutdown_hev_tx, 0)
mqttc.subscribe(alert_level_hev_tx, 0)

# Publish a message
# mqttc.publish(topic, "my message")

# Continue the network loop, exit when an error occurs
rc = 0
while True:
    rc = mqttc.loop()   # keep network traffic flow with the broker
    # mqttc.publish(credit_purchased_server_tx, json.dumps(credit_purchased_data_tx))   # publish credit purchased
    time.sleep(15)
    print(f"rc: {rc}")
    if rc != 0:
        break
print("rc end: " + str(rc))