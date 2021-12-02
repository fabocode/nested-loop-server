import requests, json

class Notifications:
    
    def __init__(self, url):
        self.url = url # address of the HEV server

    def credit_purchased(self, id, message):
        url = self.url + '/hev/' + str(id) + '/credits/credit_purchased'
        message = json.dumps(message)
        response = requests.post(url, message, headers={"Content-Type": "application/json"})
        return response.text
