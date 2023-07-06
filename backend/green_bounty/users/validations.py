# Validation Utils
from typing import Dict


def clean_data(data):
    """ cleans up the request data """
    clean = {
        'email': data.get('email'),
        'password': data.get('password'),
    }

    return clean


def tidy_data(data, token):
    """ tidy the login return data """
    clean = {
        "user": {
            'id': data.get('id'),
            'last_login': data.get('last_login'),
            'user_id': data.get('userid'),
            'email': data.get('email'),
            'date_joined': data.get('date_joined')
        },
        "user_token": token
    }

    return clean
