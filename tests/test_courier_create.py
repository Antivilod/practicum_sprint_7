import requests
import allure
import pytest
from data import data
from urls import urls
from helpers.base_helper import generate_random_string
from helpers.courier_helper import (
    register_new_courier_and_return_login_password,
    login_courier,
    delete_courier
)

@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        courier_data = register_new_courier_and_return_login_password()
        courier_id = login_courier(courier_data)
        assert courier_id is not None
        delete_courier(courier_id)

    @allure.title("Создание двух одинаковых курьеров - ошибка 409")
    def test_create_two_identical_couriers_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        courier_id = login_courier(courier_data)
        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"],
            "firstName": courier_data["firstName"]
        }
        response = requests.post(data.BASE_URL + urls.COURIER_CREATE, json=payload)
        assert response.status_code == 409
        assert response.json()["message"] == data.COURIER_CREATE_CONFLICT
        delete_courier(courier_id)

    @allure.title("Создание курьера без обязательного поля login - ошибка 400")
    def test_create_courier_missing_login_fails(self):
        payload = {
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(data.BASE_URL + urls.COURIER_CREATE, json=payload)
        assert response.status_code == 400
        assert response.json()["message"] == data.COURIER_CREATE_MISSING_DATA

    @allure.title("Создание курьера без обязательного поля password - ошибка 400")
    def test_create_courier_missing_password_fails(self):
        payload = {
            "login": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(data.BASE_URL + urls.COURIER_CREATE, json=payload)
        assert response.status_code == 400
        assert response.json()["message"] == data.COURIER_CREATE_MISSING_DATA

    @allure.title("Создание курьера без поля firstName - успех (поле необязательное)")
    def test_create_courier_missing_first_name_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        payload = {"login": login, "password": password}
        response = requests.post(data.BASE_URL + urls.COURIER_CREATE, json=payload)
        assert response.status_code == 201

    @allure.title("Создание курьера с уже существующим логином - ошибка 409")
    def test_create_courier_with_existing_login_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        courier_id = login_courier(courier_data)
        new_payload = {
            "login": courier_data["login"],
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(data.BASE_URL + urls.COURIER_CREATE, json=new_payload)
        assert response.status_code == 409
        assert response.json()["message"] == data.COURIER_CREATE_CONFLICT
        delete_courier(courier_id)