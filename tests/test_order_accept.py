import requests
import pytest
from data import data
from helpers.courier_helper import register_new_courier_and_return_login_password, login_courier, delete_courier
from helpers.order_helper import generate_order_data

class TestAcceptOrder:
    def test_accept_order_success(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        order_data = generate_order_data()
        create_response = requests.post(data.BASE_URL + data.ORDERS_CREATE, json=order_data)
        assert create_response.status_code == 201
        track = create_response.json()["track"]
        track_response = requests.get(data.BASE_URL + data.ORDERS_TRACK, params={"t": track})
        assert track_response.status_code == 200
        order_id = track_response.json()["order"]["id"]
        accept_url = data.BASE_URL + data.ORDERS_ACCEPT + str(order_id)
        response = requests.put(accept_url, params={"courierId": courier_id})
        assert response.status_code == 200
        assert response.json() == {"ok": True}
        delete_courier(courier_id)

    def test_accept_order_without_courier_id_fails(self):
        order_data = generate_order_data()
        create_response = requests.post(data.BASE_URL + data.ORDERS_CREATE, json=order_data)
        assert create_response.status_code == 201
        track = create_response.json()["track"]
        track_response = requests.get(data.BASE_URL + data.ORDERS_TRACK, params={"t": track})
        order_id = track_response.json()["order"]["id"]
        accept_url = data.BASE_URL + data.ORDERS_ACCEPT + str(order_id)
        response = requests.put(accept_url)  # без courierId
        assert response.status_code == 400
        assert response.json()["message"] == data.ORDER_ACCEPT_MISSING_DATA

    def test_accept_order_with_invalid_courier_id_fails(self):
        order_data = generate_order_data()
        create_response = requests.post(data.BASE_URL + data.ORDERS_CREATE, json=order_data)
        assert create_response.status_code == 201
        track = create_response.json()["track"]
        track_response = requests.get(data.BASE_URL + data.ORDERS_TRACK, params={"t": track})
        order_id = track_response.json()["order"]["id"]
        invalid_courier_id = 999999999
        accept_url = data.BASE_URL + data.ORDERS_ACCEPT + str(order_id)
        response = requests.put(accept_url, params={"courierId": invalid_courier_id})
        assert response.status_code == 404
        assert response.json()["message"] == data.ORDER_ACCEPT_COURIER_NOT_FOUND

    def test_accept_order_without_order_id_fails(self):
        accept_url = data.BASE_URL + data.ORDERS_ACCEPT
        response = requests.put(accept_url, params={"courierId": 1})
        assert response.status_code == 404

    def test_accept_order_with_invalid_order_id_fails(self):
        # Создаём курьера, чтобы запрос был валидным по курьеру
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        # Используем заведомо несуществующий ID заказа
        invalid_order_id = 999999999
        accept_url = data.BASE_URL + data.ORDERS_ACCEPT + str(invalid_order_id)
        response = requests.put(accept_url, params={"courierId": courier_id})
        # Ожидаем 404 Not Found
        assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"

        delete_courier(courier_id)