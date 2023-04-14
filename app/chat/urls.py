from django.urls import path
from .views import chat_room, submit_message, login, edit_message

app_name = 'chat'

# Endpoint configuration
urlpatterns = [
    path('', chat_room, name='chat_room'),
    path('submit_message', submit_message, name='submit_message'),
    path('edit_message/<int:message_id>/', edit_message, name='edit_message'),
    path('login', login, name='login'),
]