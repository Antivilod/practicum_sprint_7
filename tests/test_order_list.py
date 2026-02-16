import requests
from data import data

class TestOrderList:
    def test_get_orders_list(self):
        response = requests.get(data.BASE_URL + data.ORDERS_LIST)
        assert response.status_code == 200
        json_response = response.json()
        assert "orders" in json_response
        assert isinstance(json_response["orders"], list)