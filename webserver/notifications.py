import requests, json

class Notifications:
    
    def __init__(self, url):
        self.url = url # address of the HEV server

    def credit_purchased(self, id, message, url):
        message = json.dumps(message)
        response = requests.post(url, message, headers={"Content-Type": "application/json"})
        return response

class Messages:
    def __init__(self, url):
        self.url = url # address of the HEV server

    def hev_data(self):
        url = self.url + '/hev/messages/hev_data'
