import random
import string

ALPHABET = string.ascii_letters + string.digits  # a-zA-Z0-9

def generate_code(length=6):
    return ''.join(random.choices(ALPHABET, k=length))
