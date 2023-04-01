from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Message, User
from .lib import verify_jwt_token, generate_jwt_token


# @login_required
def chat_room(request):
    messages = Message.objects.all()
    jwt_token = request.COOKIES.get('jwt_token')
    show_popup = True
    if jwt_token is not None and verify_jwt_token(jwt_token) is not None:
        show_popup = False

    context = {
        'show_popup': show_popup,  # Set this to True to show the popup
        'messages': messages # Set array of messages to display
    }
    return render(request, 'chat_room.html', context)


def submit_message(request):
    if request.method == 'POST':
        jwt_token = request.COOKIES.get('jwt_token')

        if not jwt_token: current_user = 0
        else: current_user = verify_jwt_token(jwt_token)[0]

        message_text = request.POST.get('message_text')
        message = Message(text=message_text, user=current_user)
        message.save()

        return HttpResponseRedirect('/')
    else:
        return HttpResponseBadRequest()
    

def login(request):
    if request.method == 'POST':
        # get user info from form
        
        username = request.POST['username']
        # create user object
        user = User(username=username)
        user.save()
        
        data = {
            "user_id": user.id,
            "username": user.username
        }
        token = generate_jwt_token(data)
        # Return token in json
        return JsonResponse({"token":token})
    return HttpResponseBadRequest()
