import jwt
from django.conf import settings

def verify_jwt_token(token):
    try:
        decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_payload['user_id']
        username = decoded_payload['username']
        return user_id, username
    except jwt.exceptions.DecodeError:
        return 0, None