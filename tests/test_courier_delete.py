import requests
import allure
from data import data
from urls import urls
from helpers.courier_helper import register_new_courier_and_return_login_password, login_courier, delete_courier

@allure.feature("Удаление курьера")
class TestDeleteCourier:

    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self):
        courier_data = register_new_courier_and_return_login_password()
        courier_id = login_courier(courier_data)
        response = delete_courier(courier_id)
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Удаление курьера без указания ID - ошибка 404")
    def test_delete_courier_without_id(self):
        response = requests.delete(data.BASE_URL + urls.COURIER_DELETE)
        assert response.status_code == 404

    @allure.title("Удаление несуществующего курьера - ошибка 404")
    def test_delete_nonexistent_courier(self):
        nonexistent_id = 999999999
        response = delete_courier(nonexistent_id)
        assert response.status_code == 404
        assert response.json()["message"] == data.COURIER_DELETE_NOT_FOUND