# helpers/order_helper.py
import random
import string
from helpers.base_helper import generate_random_string

def generate_order_data():
    return {
        "firstName": generate_random_string(8),
        "lastName": generate_random_string(8),
        "address": generate_random_string(15),
        "metroStation": random.randint(1, 20),
        "phone": "+7" + ''.join(random.choice(string.digits) for _ in range(10)),
        "rentTime": random.randint(1, 7),
        "deliveryDate": "2023-12-01",
        "comment": generate_random_string(12)
    }