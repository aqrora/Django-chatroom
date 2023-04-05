from .models import User

def find_user_by_id(user_id):
    print("User_id is ", user_id)
    if user_id == None: return None
    try:
        users = User.objects.all()
        print(users)
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None