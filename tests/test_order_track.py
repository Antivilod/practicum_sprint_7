import requests
import allure
from data import data
from urls import urls
from helpers.order_helper import generate_order_data

@allure.feature("Получение заказа по номеру (треку)")
class TestOrderTrack:

    @allure.title("Получение заказа по существующему треку - успех")
    def test_get_order_by_track_success(self):
        order_data = generate_order_data()
        create_response = requests.post(data.BASE_URL + urls.ORDERS_CREATE, json=order_data)
        assert create_response.status_code == 201
        track = create_response.json()["track"]
        response = requests.get(data.BASE_URL + urls.ORDERS_TRACK, params={"t": track})
        assert response.status_code == 200
        json_response = response.json()
        assert "order" in json_response
        assert json_response["order"]["track"] == track

    @allure.title("Получение заказа без указания трека - ошибка 400")
    def test_get_order_without_track_fails(self):
        response = requests.get(data.BASE_URL + urls.ORDERS_TRACK)
        assert response.status_code == 400
        assert response.json()["message"] == data.ORDER_TRACK_MISSING_DATA

    @allure.title("Получение заказа с несуществующим треком - ошибка 404")
    def test_get_order_with_nonexistent_track_fails(self):
        nonexistent_track = 999999999
        response = requests.get(data.BASE_URL + urls.ORDERS_TRACK, params={"t": nonexistent_track})
        assert response.status_code == 404
        assert response.json()["message"] == data.ORDER_TRACK_NOT_FOUND