import requests
from flask import make_response, jsonify


class DisplayQR:
    @staticmethod
    def post_create_qr_code():

        api_key = False
        url = 'http://localhost:5001/create_qr_code'
        response = requests.request("POST", url=url, data=api_key)
        if not response:
            return 401
        else:
            return response.status_code == 200 or response.status_code == 201

    @staticmethod
    def post_make_qr(api_key):
        headers = {
            'Authorization': 'Basic ' + api_key
        }
        url = 'http://localhost:5001/create_qr_code'
        response = requests.request("POST", url=url, headers=headers)
        if not response:
            return 401
        else:
            return response.status_code == 200 or response.status_code == 201

    @staticmethod
    def get_qr_code():
        url = 'http://display_serv:5001/get_qr_code'
        response = requests.request("GET", url=url)
        if not response:
            return 401
        else:
            return response.json()  # return the qr code

    @staticmethod
    def retrieve_qr_code(api_key):
        headers = {
            'Authorization': 'Basic ' + api_key
        }
        url = 'http://display_serv:5001/get_qr_code'
        response = requests.request("GET", url=url, headers=headers)
        if not response:
            return 401
        else:
            return response.json()  # return the qr code

    @staticmethod
    def del_delete_qr_code():
        url = 'http://display_serv:5001/delete_qr_code'
        api_key = False
        response = requests.request("DELETE", url=url, data=api_key)
        response_json = response.json()
        if not response_json:
            return 401
        else:
            return response_json['message'] == 'Qr code deleted' or response_json['message'] == 'Qr code does not exist'

    @staticmethod
    def put_update_qr_code():
        url = 'http://display_serv:5001/update_qr_code'
        api_key = False
        response = requests.request("PUT", url=url, data=api_key)
        response_json = response.json()
        if not response_json:
            return 401
        else:
            return response_json['message'] == 'Qr code updated' or response_json['message'] == 'Qr code does not exist'
