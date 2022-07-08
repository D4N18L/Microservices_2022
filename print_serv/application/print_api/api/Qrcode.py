import requests
from flask import session


class Qrcode:
    @staticmethod
    def check_qr_to_print():
        """
        Check if the QR code is in the database
        :param qr_code: The QR code to check
        :return: True if the QR code is in the database, False otherwise
        """
        response = requests.request("GET", "http://localhost:5001/get_qr_code")

        if response.status_code == 401:
            return False
        else:
            return True
