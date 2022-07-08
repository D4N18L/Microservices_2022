import requests


class Holder:
    @staticmethod
    def get_holder(api_key):
        headers = {
            'Authorization': api_key
        }  # headers gets the api_key from the request header
        response = requests.request("GET", url='http://container_register_serv:5000/user', headers=headers)

        if response.status_code == 401:
            return False
        user = response.json()  # user is the json response from the register_serv
        return user


