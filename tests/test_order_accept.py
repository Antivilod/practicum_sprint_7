import requests
import allure
from data import data
from urls import urls
from helpers.order_helper import generate_order_data
from helpers.courier_helper import (
    register_new_courier_and_return_login_password,
    login_courier,
    delete_courier
)

@allure.feature("Принятие заказа")
class TestAcceptOrder:

    @allure.title("Успешное принятие заказа курьером")
    def test_accept_order_success(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        order_data = generate_order_data()
        create_response = requests.post(data.BASE_URL + urls.ORDERS_CREATE, json=order_data)
        assert create_response.status_code == 201
        track = create_response.json()["track"]
        track_response = requests.get(data.BASE_URL + urls.ORDERS_TRACK, params={"t": track})
        assert track_response.status_code == 200
        order_id = track_response.json()["order"]["id"]
        accept_url = data.BASE_URL + urls.ORDERS_ACCEPT + str(order_id)
        response = requests.put(accept_url, params={"courierId": courier_id})
        assert response.status_code == 200
        assert response.json() == {"ok": True}
        delete_courier(courier_id)

    @allure.title("Принятие заказа без указания courierId - ошибка 400")
    def test_accept_order_without_courier_id_fails(self):
        order_data = generate_order_data()
        create_response = requests.post(data.BASE_URL + urls.ORDERS_CREATE, json=order_data)
        assert create_response.status_code == 201
        track = create_response.json()["track"]
        track_response = requests.get(data.BASE_URL + urls.ORDERS_TRACK, params={"t": track})
        order_id = track_response.json()["order"]["id"]
        accept_url = data.BASE_URL + urls.ORDERS_ACCEPT + str(order_id)
        response = requests.put(accept_url)
        assert response.status_code == 400
        assert response.json()["message"] == data.ORDER_ACCEPT_MISSING_DATA

    @allure.title("Принятие заказа с несуществующим courierId - ошибка 404")
    def test_accept_order_with_invalid_courier_id_fails(self):
        order_data = generate_order_data()
        create_response = requests.post(data.BASE_URL + urls.ORDERS_CREATE, json=order_data)
        assert create_response.status_code == 201
        track = create_response.json()["track"]
        track_response = requests.get(data.BASE_URL + urls.ORDERS_TRACK, params={"t": track})
        order_id = track_response.json()["order"]["id"]
        invalid_courier_id = 999999999
        accept_url = data.BASE_URL + urls.ORDERS_ACCEPT + str(order_id)
        response = requests.put(accept_url, params={"courierId": invalid_courier_id})
        assert response.status_code == 404
        assert response.json()["message"] == data.ORDER_ACCEPT_COURIER_NOT_FOUND

    @allure.title("Принятие заказа без указания orderId - ошибка 404")
    def test_accept_order_without_order_id_fails(self):
        accept_url = data.BASE_URL + urls.ORDERS_ACCEPT
        response = requests.put(accept_url, params={"courierId": 1})
        assert response.status_code == 404

    @allure.title("Принятие заказа с несуществующим orderId - ошибка 404")
    def test_accept_order_with_invalid_order_id_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data is not None
        courier_id = login_courier(courier_data)
        invalid_order_id = 999999999
        accept_url = data.BASE_URL + urls.ORDERS_ACCEPT + str(invalid_order_id)
        response = requests.put(accept_url, params={"courierId": courier_id})
        assert response.status_code == 404
        delete_courier(courier_id)