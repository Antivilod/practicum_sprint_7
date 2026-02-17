import pytest
import allure
from helpers.courier_helper import register_new_courier_and_return_login_password, login_courier, delete_courier

@pytest.fixture
@allure.step("Создание курьера и его удаление после теста")
def courier():
    courier_data = register_new_courier_and_return_login_password()
    assert courier_data is not None, "Не удалось создать курьера"
    courier_id = login_courier(courier_data)
    assert courier_id is not None, "Не удалось авторизоваться"
    yield (courier_data, courier_id)   # именно кортеж
    delete_courier(courier_id)