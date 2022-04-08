from flask import Flask, request, render_template, redirect, url_for
from flask_restful import Resource, Api, reqparse
import requests
from notifications import Notifications
import json

app = Flask(__name__)
api = Api(app)

hev_ip_address = 'http://192.168.1.7:5000'  # provisional ip address to communicate between servers (pi and server)
notifications = Notifications(hev_ip_address)   

# messages
class Credit_Purchased(Resource):
    
    def post(self, serial_number):
        url = hev_ip_address + request.path
        print(url)
        print(f"bytes in requests: {request.headers['Content-Length']}")
        data = request.get_json()
        data = json.dumps(data)
        response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
        if response.status_code == 201:
            return response.json(), 201
        else:
            return response.text

class Hev_Data(Resource):

    def set_hev_data(self, hev_data):
        self.hev_data = hev_data

    def get_hev_data(self):
        return self.hev_data

    def get(self, id):
        url = hev_ip_address + request.path
        print(f"bytes in requests: {request.headers['Content-Length']}")
        response = requests.get(url)
        print(f"response in bytes: {len(response.content)}")
        print(f"response: {response.json()}")
        return response.json()

class Block_Technician(Resource):

    def post(self, serial_number):
        print(f"bytes in requests: {request.headers['Content-Length']}")
        url = hev_ip_address + request.path
        print(url)
        data = request.get_json()
        data = json.dumps(data)
        print(data)
        response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
        print(f"response in bytes: {len(response.content)}")
        if response.status_code == 201:
            return response.json(), 201
        else:
            return response.text

class HEV_Shutdown(Resource):

    def post(self, serial_number):
        print(f"bytes in requests: {request.headers['Content-Length']}")
        url = hev_ip_address + request.path
        data = request.get_json()
        data = json.dumps(data)
        print("data shutdown: ", data)
        response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
        print(f"response in bytes: {len(response.content)}")
        if response.status_code == 201:
            return response.json(), 201
        else:
            return response.text

class HEV_Resume(Resource):

    def post(self, serial_number):
        print(f"bytes in requests: {request.headers['Content-Length']}")
        url = hev_ip_address + request.path
        data = request.get_json()
        data = json.dumps(data)
        print("data shutdown: ", data)
        response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
        print(f"response in bytes: {len(response.content)}")
        if response.status_code == 201:
            return response.json(), 201
        else:
            return response.text

# notifications 
class Serial_Number(Resource):
    
    def post(self):
        print(f"bytes in requests: {request.headers['Content-Length']}")
        json_data = request.get_json()
        if json_data['msg_code'] == 0x65:
            return {'Server response': 'ACK'}, 201  
        else:
            return {'Server response': 'NACK - invalid msg code'}, 201

class Technician_Request(Resource):
    def post(self):
        print(f"bytes in requests: {request.headers['Content-Length']}")
        json_data = request.get_json()
        if json_data['msg_code'] == 0x66:
            print(f"{json_data['msg_code']} - {json_data['data']}")
            return {'Server response': 'ACK'}, 201  
        else:
            return {'Server response': 'NACK - invalid msg code'}, 201

class Thermal_Shutdown(Resource):
    def post(self):
        print(f"bytes in requests: {request.headers['Content-Length']}")
        json_data = request.get_json()
        if json_data['msg_code'] == 0x67:
            print(f"{json_data['msg_code']} - {json_data['data']}")
            return {'Server response': 'ACK'}, 201  
        else:
            return {'Server response': 'NACK - invalid msg code'}, 201

class Alert_Level(Resource):
    def post(self):
        print(f"bytes in requests: {request.headers['Content-Length']}")
        json_data = request.get_json()
        if json_data['msg_code'] == 0x68:
            print(f"{json_data['msg_code']} - {json_data['data']}")
            return {'Server response': 'ACK'}, 201  
        else:
            return {'Server response': 'NACK - invalid msg code'}, 201

class Sleep_Mode(Resource):
    def post(self):
        print(f"bytes in requests: {request.headers['Content-Length']}")
        json_data = request.get_json()
        if json_data['msg_code'] == 0x69:
            print(f"{json_data['msg_code']} - {json_data['data']}")
            return 201  
        else:
            return {'Server response': 'NACK - invalid msg code'}, 201

class Critical_Alert(Resource):
    def post(self):
        print(f"bytes in requests: {request.headers['Content-Length']}")
        json_data = request.get_json()
        if json_data['msg_code'] == 0x6A:
            print(f"{json_data['msg_code']} - {json_data['data']}")
            return 201  
        else:
            return {'Server response': 'NACK - invalid msg code'}, 201

class Credit_Low(Resource):
    def post(self):
        print(f"bytes in requests: {request.headers['Content-Length']}")
        json_data = request.get_json()
        if json_data['msg_code'] == 0x6B:
            print(f"{json_data['msg_code']} - {json_data['data']}")
            return {'Server response': 'ACK'}, 201  
        else:
            return {'Server response': 'NACK - invalid msg code'}, 201

class Fire_Alert(Resource):
    def post(self):
        print(f"bytes in requests: {request.headers['Content-Length']}")
        json_data = request.get_json()
        if json_data['msg_code'] == 0x6C:
            print(f"{json_data['msg_code']} - {json_data['data']}")
            return {'Server response': 'ACK'}, 201  
        else:
            return {'Server response': 'NACK - invalid msg code'}, 201\

class Access_Granted(Resource):
    def post(self):
        print(f"bytes in requests: {request.headers['Content-Length']}")
        json_data = request.get_json()
        if json_data['msg_code'] == 0x6D:
            print(f"{json_data['msg_code']} - {json_data['data']}")
            return {'Server response': 'ACK'}, 201  
        else:
            return {'Server response': 'NACK - invalid msg code'}, 201


@app.route('/')
def index():
    return "hello world from server"




# messages from server to hev
api.add_resource(Credit_Purchased,      '/api/notification/hev/<int:serial_number>/credits/credit_purchased')       
api.add_resource(Hev_Data,              '/api/message/hev/<int:id>/hev_data')
api.add_resource(Block_Technician,      '/api/message/hev/<int:serial_number>/block_technician')
# message from server to HEV
api.add_resource(Serial_Number,         '/api/notification/server/serial_number')       # from server to HEV
api.add_resource(HEV_Shutdown,          '/api/message/hev/<int:serial_number>/shutdown')        # from server to HEV
api.add_resource(HEV_Resume,          '/api/message/hev/<int:serial_number>/resume')        # from server to HEV
api.add_resource(Technician_Request,    '/api/notification/server/technician_request')  
api.add_resource(Thermal_Shutdown,      '/api/notification/server/thermal_shutdown')
api.add_resource(Alert_Level,           '/api/notification/server/alert_level')
api.add_resource(Sleep_Mode,            '/api/notification/server/sleep_mode')
api.add_resource(Critical_Alert,        '/api/notification/server/critical_alert')
api.add_resource(Credit_Low,            '/api/notification/server/credit_low')
api.add_resource(Fire_Alert,            '/api/notification/server/fire_alert')
api.add_resource(Access_Granted,        '/api/notification/server/access_granted')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
