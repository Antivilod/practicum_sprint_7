import requests
import allure
from data import data
from urls import urls

@allure.feature("Получение списка заказов")
class TestOrderList:

    @allure.title("Получение списка заказов - успешный запрос")
    def test_get_orders_list(self):
        response = requests.get(data.BASE_URL + urls.ORDERS_LIST)
        assert response.status_code == 200
        json_response = response.json()
        assert "orders" in json_response
        assert isinstance(json_response["orders"], list)