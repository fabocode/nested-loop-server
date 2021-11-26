import os
from urllib.parse import urlparse   # to get the hostname from the url on .env
import yaml

class MQTT_Config:

    def __init__(self):
        # Parse CLOUDMQTT_URL from .env (or fallback to localhost)
        self.url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
        self.url = urlparse(self.url_str)
        self.hostname = self.url.hostname
        self.port = self.url.port
        self.username = self.url.username
        self.password = self.url.password
        
        # Load the config file (yaml file)
        with open('mqtt_conf.yaml') as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
            
            # ID of the device
            self.cliend_id = self.config.get('ids')["client"]
            self.server_id = self.config.get('ids')["server"]
            
            # topics
            # requests
            self.hev_data_req_topic = self.config.get('topics')["hev_data"]
            self.block_technician_req_topic = self.config.get('topics')["block_technician"]
            self.hev_shutdown_req_topic = self.config.get('topics')["hev_shutdown"]
            self.hev_resume_req_topic = self.config.get('topics')["hev_resume"]

            # topics
            # notifications 
            self.credit_purchased_notif_topic = self.config.get('topics')["credit_purchased"]
            self.serial_number_notif_topic = self.config.get('topics')["serial_number"]
            self.technician_notif_topic = self.config.get('topics')["technician_request"]
            self.thermal_shutdown_notif_topic = self.config.get('topics')["thermal_shutdown"]
            self.alert_level_notif_topic = self.config.get('topics')["alert_level"]
            self.sleep_mode_notif_topic = self.config.get('topics')["sleep_mode"]
            self.critical_alert_notif_topic = self.config.get('topics')["critical_alert"]
            self.credit_low_notif_topic = self.config.get('topics')["credit_low"]
            self.fire_alarm_notif_topic = self.config.get('topics')["fire"]
            self.access_granted_notif_topic = self.config.get('topics')["access_granted"]

            # codes 
            self.code_hev_data_req = self.config.get('codes')["hev_data"]
            self.code_block_technician_req = self.config.get('codes')["block_technician"]
            self.code_hev_shutdown_req = self.config.get('codes')["hev_shutdown"]
            self.code_hev_resume_req = self.config.get('codes')["hev_resume"]

            # notifications 
            self.code_credit_purchased = self.config.get('codes')["credit_purchased"]
            self.code_serial_number = self.config.get('codes')["serial_number"]
            self.code_technician_request = self.config.get('codes')["technician_request"]
            self.code_thermal_shutdown = self.config.get('codes')["thermal_shutdown"]
            self.code_alert_level = self.config.get('codes')["alert_level"]
            self.code_sleep_mode = self.config.get('codes')["sleep_mode"]
            self.code_critical_alert = self.config.get('codes')["critical_alert"]
            self.code_credit_low = self.config.get('codes')["credit_low"]
            self.code_fire_alarm = self.config.get('codes')["fire"]
            self.code_access_granted = self.config.get('codes')["access_granted"]
            
