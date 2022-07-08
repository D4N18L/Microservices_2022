import requests
from flask import session


class Holder:
    @staticmethod
    def post_login(form):
        api_key = False
        #api_key = "$5$rounds=535000$/6iRrqSdXM2So3oX$SexfPLCG1i9oboqph7ByJDJrj5WI2LlSPqbLwPmpjV7"
        payload = {
            'username': form.username.data,
            'password': form.password.data
        }

        url = 'http://register_serv:5000/login'
        response = requests.request("POST",url=url,data=payload)
        if response:
            response_json = response.json()
            if response_json['message'] == 'User logged in successfully':
                api_key = response_json['user']['api_key']
        return api_key

    @staticmethod
    def get_user():
        headers = {
            'Authorization': 'Basic ' + session['api_key']
        }
        url = 'http://register_serv:5000/user'
        response = requests.request("GET",url=url,headers=headers)
        holder = response.json()
        return holder

    @staticmethod
    def get_users():
        api_key = False
        #api_key = "$5$rounds=535000$twu9x9j.Ey2NOFhG$oQOuZFjzepFOTfAcdGQnBXz.6hiGZcNuguC8NLhjy52"
        headers = {
            'Authorization': 'Basic ' + session['api_key']
        }
        url = 'http://register_serv:5000/get_users'
        response = requests.request("GET",url=url,headers=headers)
        holders = response.json()
        return holders

    @staticmethod
    def post_create(form):
        holder = False
        payload = {
            'username': form.username.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data,
            'password': form.password.data
        }
        url = 'http://register_serv:5000/create_user'
        response = requests.request("POST",url=url,data=payload)
        if response:
            holder = response.json()
        return holder

    @staticmethod
    def post_logout():
        session.clear()
        return True

    @staticmethod
    def get_username_exists(username):
        payload = {
            'username': username
        }
        url = 'http://register_serv:5000/user/' + username + '/exists'
        response = requests.request("GET",url=url,data=payload)
        return response.status_code == 200



    @staticmethod
    def get_username_active(username):
        url = 'http://register_serv:5000/' + username + '/active'
        response = requests.request("GET",url=url)
        return response.status_code == 200

    @staticmethod
    def del_remove_user(username):
        url = 'http://register_serv:5000/remove_user/'
        response = requests.request("DELETE",url=url,data={'username':username})
        return response.json()

    @staticmethod
    def del_remove_all_users():
        url = 'http://register_serv:5000/remove_all'
        response = requests.request("DELETE",url=url)
        return response.json()

    @staticmethod
    def post_save_img():
        url = 'http://register_serv:5000/save_img'
        response = requests.request("POST",url=url)
        return response.status_code == 200









