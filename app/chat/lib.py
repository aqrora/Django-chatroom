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