import requests
import random
import string
from data import data

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def register_new_courier_and_return_login_password():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(data.BASE_URL + data.COURIER_CREATE, json=payload)
    if response.status_code == 201:
        return {
            "login": login,
            "password": password,
            "firstName": first_name,
            "id": None
        }
    else:
        return None

def login_courier(credentials):
    payload = {
        "login": credentials["login"],
        "password": credentials["password"]
    }
    response = requests.post(data.BASE_URL + data.COURIER_LOGIN, json=payload)
    if response.status_code == 200:
        return response.json()["id"]
    return None

def delete_courier(courier_id):
    url = data.BASE_URL + data.COURIER_DELETE + str(courier_id)
    response = requests.delete(url)
    return response