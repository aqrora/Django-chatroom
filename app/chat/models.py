from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone




class User(AbstractUser):
    username = models.CharField(max_length=32)
    joined = models.DateTimeField(default = timezone.now)
    color = models.CharField(max_length=7, default = '#000000')
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
    # id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default = timezone.now)
    
