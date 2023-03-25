from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

# @login_required
def chat_room(request):
    messages = Message.objects.all()
    return render(request, 'chat_room.html', {'messages': messages})