<<<<<<< HEAD
<<<<<<< HEAD
from django.urls import path
from .views import chat_room, submit_message, login

app_name = 'chat'

urlpatterns = [
    path('', chat_room, name='chat_room'),
    path('submit_message', submit_message, name='submit_message'),
    path('login', login, name='login'),
=======
from django.urls import path
from .views import chat_room, test_socket, submit_message, login

app_name = 'chat'

urlpatterns = [
    path('', chat_room, name='chat_room'),
    path('test_socket', test_socket, name='test_socket'),
    path('submit_message', submit_message, name='submit_message'),
    path('login', login, name='login'),
>>>>>>> 090aff871ce41a98081ffc8fa49023aefbb4e6e3
=======
from django.urls import path
from .views import chat_room, submit_message, login, edit_message

app_name = 'chat'

# Endpoint configuration
urlpatterns = [
    path('', chat_room, name='chat_room'),
    path('submit_message', submit_message, name='submit_message'),
    path('edit_message/<int:message_id>/', edit_message, name='edit_message'),
    path('login', login, name='login'),
>>>>>>> origin/master
]