import requests
import allure
import pytest
from data import data
from urls import urls
from helpers.order_helper import generate_order_data

@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с различными цветами самоката")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_color(self, color):
        order_data = generate_order_data()
        order_data["color"] = color
        response = requests.post(data.BASE_URL + urls.ORDERS_CREATE, json=order_data)
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)