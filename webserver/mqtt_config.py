import yaml 

class MQTTConfig:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config                 = yaml.load(f, Loader=yaml.FullLoader)
            self.broker_address         = self.config.get('FLESPI_MQTT')["HOSTNAME"]
            self.port                   = int(self.config.get('FLESPI_MQTT')["PORT"])
            self.username               = self.config.get('FLESPI_MQTT')["USERNAME"]
            self.password               = str(self.config.get('FLESPI_MQTT')["PASSWORD"])
            self.id                     = self.config.get('HEV')["ID"]
            self.client_name            = self.config.get('HEV')["CLIENT_NAME"]
            self.credit_purchased_pub   = self.config.get('NOTIFICATIONS')["CREDIT_PURCHASED_PUB"]
            self.credit_purchased_resp  = self.config.get('NOTIFICATIONS')["CREDIT_PURCHASED_SUB"]

    def get_credit_purchased_pub(self):
        return self.credit_purchased_pub

    def get_credit_purchased_resp(self):
        return self.credit_purchased_resp

    def get_broker_address(self):
        return self.broker_address

    def get_port(self):
        return self.port

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_id(self):
        return self.id
