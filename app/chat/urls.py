from django.urls import path
from .views import chat_room, submit_message, login

app_name = 'chat'

urlpatterns = [
    path('', chat_room, name='chat_room'),
    path('submit_message', submit_message, name='submit_message'),
    path('login', login, name='login'),
]