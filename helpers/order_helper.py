import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

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