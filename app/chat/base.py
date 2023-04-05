from .models import User

def find_user_by_id(user_id):
    print(user_id)
    users = User.objects.all()
    print(users)
    user = User.objects.get(id=user_id)
    return user
