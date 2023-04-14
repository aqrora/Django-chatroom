from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone




class User(AbstractUser):
    username = models.CharField(max_length=32)
    joined = models.DateTimeField(default = timezone.now)
    color = models.CharField(max_length = 7, default = '#000000')
    avatar = models.CharField(max_length = 100, default="https://miramarvet.com.au/wp-content/uploads/2021/08/api-cat2.jpg")
    date_joined = None
    first_name = None
    last_name = None
    email = None
    is_staff = None
    is_superuser = None
    last_login = None
    password = None
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='auth_users',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='auth_users',
        blank=True,
    )

class Message(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default = timezone.now)
    edited = models.BooleanField(default = False)
