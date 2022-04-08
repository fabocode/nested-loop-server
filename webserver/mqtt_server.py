from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from uuid import uuid4
import json
import threading

'''
usage: https_sample.py [-h] --endpoint ENDPOINT --cert CERT --key KEY --topic TOPIC
                       [--message MESSAGE]
'''

class MQTT_Server:

    def __init__(self, endpoint, cert, key, topic):
        self.endpoint = endpoint
        self.cert = cert
        self.key = key
        self.topic = topic
        self.proxy_options = None
        self.client_id = "test-" + str(uuid4())
        received_count = 0
        received_all_event = threading.Event()
        self.mqtt_connection = None

    def connect(self):
        # Create an IoT endpoint using MQTT.
        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.endpoint,
            cert_filepath=self.cert,
            pri_key_filepath=self.key,
            ca_filepath=self.ca_file,
            on_connection_interrupted=self.on_connection_interrupted,
            on_connection_resumed=self.on_connection_resumed,
            client_id=self.client_id,
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=self.proxy_options)

        print("Connecting to {} with client ID '{}'...".format(self.endpoint, self.client_id))

        self.connect_future = self.mqtt_connection.connect()

        # Future.result() waits until a result is available
        self.connect_future.result()
        print("Connected!")

    def disconnect(self):
        print("Disconnecting...")
        disconnect_future = self.mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")

    def subscribe(self, topic):
        print("Subscribing to topic '{}'...".format(topic))
        subscribe_future, packed_id = self.mqtt_connection.subscribe(topic, qos=mqtt.QoS.AT_LEAST_ONCE, callback=self.on_message_received)
        subscribe_result = subscribe_future.result()
        print("Subscribed with {}".format(str(subscribe_result['qos'])))
        

    # Callback when connection is accidentally lost.
    def on_connection_interrupted(self, connection, error, **kwargs):
        print("Connection interrupted. error: {}".format(error))


    # Callback when an interrupted connection is re-established.
    def on_connection_resumed(self, connection, return_code, session_present, **kwargs):
        print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

        if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
            print("Session did not persist. Resubscribing to existing topics...")
            resubscribe_future, _ = connection.resubscribe_existing_topics()

            # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
            # evaluate result with a callback instead.
            resubscribe_future.add_done_callback(self.on_resubscribe_complete)


    def on_resubscribe_complete(self, resubscribe_future):
            resubscribe_results = resubscribe_future.result()
            print("Resubscribe results: {}".format(resubscribe_results))

            for topic, qos in resubscribe_results['topics']:
                if qos is None:
                    sys.exit("Server rejected resubscribe to topic: {}".format(topic))


    # Callback when the subscribed topic receives a message
    def on_message_received(self, topic, payload, dup, qos, retain, **kwargs):
        print("Received message from topic '{}': {}".format(topic, payload))
        global received_count
        received_count += 1
        if received_count == args.count:
            self.received_all_event.set()
