# helpers/courier_helper.py
import requests
import allure
from data import data
from urls import urls
from helpers.base_helper import generate_random_string

@allure.step("Регистрация нового курьера и возврат его учётных данных")
def register_new_courier_and_return_login_password():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(data.BASE_URL + urls.COURIER_CREATE, json=payload)
    if response.status_code == 201:
        return {
            "login": login,
            "password": password,
            "firstName": first_name,
            "id": None
        }
    else:
        return None

@allure.step("Логин курьера и получение его ID")
def login_courier(credentials):
    payload = {
        "login": credentials["login"],
        "password": credentials["password"]
    }
    response = requests.post(data.BASE_URL + urls.COURIER_LOGIN, json=payload)
    if response.status_code == 200:
        return response.json()["id"]
    return None

@allure.step("Удаление курьера по ID")
def delete_courier(courier_id):
    url = data.BASE_URL + urls.COURIER_DELETE + str(courier_id)
    response = requests.delete(url)
    return response