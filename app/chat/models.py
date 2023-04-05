from django.db import models
from django.contrib.auth.models import AbstractUser






class User(AbstractUser):
    username = models.CharField(max_length=32)
    joined = models.DateTimeField(auto_now=True)
    first_name = None
    last_name = None
    email = None
    
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
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    
