import requests
import pytest
from data import data
from helpers.courier_helper import (
    generate_random_string,
    register_new_courier_and_return_login_password,
    login_courier,
    delete_courier
)

class TestCreateCourier:
    def test_create_courier_success(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None, "Не удалось создать курьера"
        courier_id = login_courier(courier_data)
        assert courier_id is not None, "Не удалось авторизоваться после создания"
        delete_courier(courier_id)

    def test_create_two_identical_couriers_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"],
            "firstName": courier_data["firstName"]
        }
        response = requests.post(data.BASE_URL + data.COURIER_CREATE, json=payload)
        assert response.status_code == 409
        assert response.json()["message"] == data.COURIER_CREATE_CONFLICT
        delete_courier(courier_id)

    @pytest.mark.parametrize("missing_field,expected_status", [
        ("login", 400),
        ("password", 400),
        ("firstName", 201)
    ])
    def test_create_courier_missing_field_fails(self, missing_field, expected_status):
        full_payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        del full_payload[missing_field]
        response = requests.post(data.BASE_URL + data.COURIER_CREATE, json=full_payload)
        assert response.status_code == expected_status
        if expected_status == 400:
            assert response.json()["message"] == data.COURIER_CREATE_MISSING_DATA

    def test_create_courier_with_existing_login_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        new_payload = {
            "login": courier_data["login"],
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(data.BASE_URL + data.COURIER_CREATE, json=new_payload)
        assert response.status_code == 409
        assert response.json()["message"] == data.COURIER_CREATE_CONFLICT
        delete_courier(courier_id)