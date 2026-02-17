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

@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Успешный логин курьера")
    def test_login_courier_success(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        response = requests.post(data.BASE_URL + urls.COURIER_LOGIN, json=payload)
        assert response.status_code == 200
        assert "id" in response.json()
        delete_courier(courier_id)

    @allure.title("Логин без поля login - ошибка 400")
    @pytest.mark.flaky(reruns=3)
    def test_login_missing_login_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        payload = {"password": courier_data["password"]}
        response = requests.post(data.BASE_URL + urls.COURIER_LOGIN, json=payload)
        assert response.status_code == 400
        assert response.json()["message"] == data.COURIER_LOGIN_MISSING_DATA
        delete_courier(courier_id)

    @allure.title("Логин без поля password - ошибка 400")
    @pytest.mark.flaky(reruns=3)
    def test_login_missing_password_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        payload = {"login": courier_data["login"]}
        response = requests.post(data.BASE_URL + urls.COURIER_LOGIN, json=payload)
        assert response.status_code == 400
        assert response.json()["message"] == data.COURIER_LOGIN_MISSING_DATA
        delete_courier(courier_id)

    @allure.title("Логин с неверным паролем - ошибка 404")
    def test_login_wrong_password_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        payload = {
            "login": courier_data["login"],
            "password": "wrong" + courier_data["password"]
        }
        response = requests.post(data.BASE_URL + urls.COURIER_LOGIN, json=payload)
        assert response.status_code == 404
        assert response.json()["message"] == data.COURIER_LOGIN_NOT_FOUND
        delete_courier(courier_id)

    @allure.title("Логин несуществующего курьера - ошибка 404")
    def test_login_nonexistent_courier_fails(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }
        response = requests.post(data.BASE_URL + urls.COURIER_LOGIN, json=payload)
        assert response.status_code == 404
        assert response.json()["message"] == data.COURIER_LOGIN_NOT_FOUND