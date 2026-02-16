import requests
import pytest
from data import data
from helpers.courier_helper import (
    register_new_courier_and_return_login_password,
    login_courier,
    delete_courier,
    generate_random_string
)

class TestLoginCourier:
    def test_login_courier_success(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        assert courier_id is not None, "ID не получен при логине"
        delete_courier(courier_id)

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @pytest.mark.flaky(reruns=5)  # 5 попыток при ошибках 504
    def test_login_missing_field_fails(self, missing_field):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        del payload[missing_field]
        response = requests.post(data.BASE_URL + data.COURIER_LOGIN, json=payload)
        assert response.status_code == 400
        assert response.json()["message"] == data.COURIER_LOGIN_MISSING_DATA
        delete_courier(courier_id)

    def test_login_wrong_password_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        wrong_payload = {
            "login": courier_data["login"],
            "password": "wrong" + courier_data["password"]
        }
        response = requests.post(data.BASE_URL + data.COURIER_LOGIN, json=wrong_payload)
        assert response.status_code == 404
        assert response.json()["message"] == data.COURIER_LOGIN_NOT_FOUND
        delete_courier(courier_id)

    def test_login_nonexistent_courier_fails(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }
        response = requests.post(data.BASE_URL + data.COURIER_LOGIN, json=payload)
        assert response.status_code == 404
        assert response.json()["message"] == data.COURIER_LOGIN_NOT_FOUND