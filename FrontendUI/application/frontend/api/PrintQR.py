import requests


class PrintQR:
    @staticmethod
    def post_print_code():
        url = 'http://print_serv:5002/print_code'

        response = requests.request("POST", url=url)

        if not response:
            return 401
        else:
            return response.status_code == 200
