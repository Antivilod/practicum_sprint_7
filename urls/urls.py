# urls.py
# Относительные пути эндпоинтов API

COURIER_CREATE = "/api/v1/courier"
COURIER_LOGIN = "/api/v1/courier/login"
COURIER_DELETE = "/api/v1/courier/"  # + id
ORDERS_CREATE = "/api/v1/orders"
ORDERS_LIST = "/api/v1/orders"
ORDERS_ACCEPT = "/api/v1/orders/accept/"  # + id?courierId=...
ORDERS_TRACK = "/api/v1/orders/track"