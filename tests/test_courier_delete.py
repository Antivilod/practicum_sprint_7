import requests
import pytest
from data import data
from helpers.courier_helper import register_new_courier_and_return_login_password, login_courier, delete_courier

class TestDeleteCourier:
    def test_delete_courier_success(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        response = delete_courier(courier_id)
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    def test_delete_courier_without_id(self):
        response = requests.delete(data.BASE_URL + data.COURIER_DELETE)
        assert response.status_code == 404

    def test_delete_nonexistent_courier(self):
        nonexistent_id = 999999999
        response = delete_courier(nonexistent_id)
        assert response.status_code == 404
        assert response.json()["message"] == data.COURIER_DELETE_NOT_FOUND