<<<<<<< HEAD
import jwt
from django.conf import settings
from datetime import datetime, timedelta

def generate_jwt_token(data):
    
    # Set the token payload (e.g. user ID and username)
    payload = {'user_id': 123, 'username': 'johndoe'}

    # Generate the token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token


def verify_jwt_token(token):
    try:
        decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_payload['user_id']
        username = decoded_payload['username']
        return user_id, username
    except jwt.exceptions.DecodeError:
        return 0, None
=======
import jwt, random
from django.conf import settings
from datetime import datetime, timedelta
from . import base

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)



def generate_jwt_token(data):
    
    # Set the token payload (e.g. user ID and username)
    

    # Generate the token
    token = jwt.encode(data, settings.SECRET_KEY, algorithm='HS256')

    return token


def verify_jwt_token(token):
    try:

        decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = base.find_user_by_id(decoded_payload['user_id'])
        
        return user
    except jwt.exceptions.DecodeError:
        return None
>>>>>>> 090aff871ce41a98081ffc8fa49023aefbb4e6e3
