# helpers/base_helper.py
import random
import string

def generate_random_string(length):
    """Генерирует случайную строку заданной длины."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))