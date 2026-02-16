# Основной URL сервиса
BASE_URL = "https://qa-scooter.praktikum-services.ru"

# Эндпоинты
COURIER_CREATE = "/api/v1/courier"
COURIER_LOGIN = "/api/v1/courier/login"
COURIER_DELETE = "/api/v1/courier/"  # + id
ORDERS_CREATE = "/api/v1/orders"
ORDERS_LIST = "/api/v1/orders"
ORDERS_ACCEPT = "/api/v1/orders/accept/"  # + id?courierId=...
ORDERS_TRACK = "/api/v1/orders/track"

# Сообщения об ошибках
COURIER_CREATE_MISSING_DATA = "Недостаточно данных для создания учетной записи"
COURIER_CREATE_CONFLICT = "Этот логин уже используется. Попробуйте другой."
COURIER_LOGIN_MISSING_DATA = "Недостаточно данных для входа"
COURIER_LOGIN_NOT_FOUND = "Учетная запись не найдена"
COURIER_DELETE_MISSING_DATA = "Недостаточно данных для удаления курьера"
COURIER_DELETE_NOT_FOUND = "Курьера с таким id нет."          # точка в конце
ORDER_ACCEPT_MISSING_DATA = "Недостаточно данных для поиска"
ORDER_ACCEPT_COURIER_NOT_FOUND = "Курьера с таким id не существует"
ORDER_TRACK_MISSING_DATA = "Недостаточно данных для поиска"
ORDER_TRACK_NOT_FOUND = "Заказ не найден"

# Другие константы
COURIER_ID_NOT_FOUND_MESSAGE = "Курьер с идентификатором {courierId} не найден"