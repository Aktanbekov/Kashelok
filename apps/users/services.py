from django.utils.crypto import get_random_string


def generate_unique_code():
    code = get_random_string(4, '0123456789')
    return code
