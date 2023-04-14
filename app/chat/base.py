from .models import User, Message

def find_user_by_id(user_id):
    # Retrieves user from database. If user doesn't exists, or user_id is incorrect - returns None
    if user_id == None: return None
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None
    

def find_message_by_id(message_id):
    # Retrieves message from database. If message doesn't exists, or message_id is incorrect - returns None
    if message_id == None: return None
    try:
        msg = Message.objects.get(id=message_id)
        return msg
    except Message.DoesNotExist:
        return None