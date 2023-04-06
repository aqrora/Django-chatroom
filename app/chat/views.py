from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Message, User
from .lib import verify_jwt_token, generate_jwt_token, generate_random_color
from .forms import *



def requires_auth(view_func):
    def wrapper(request, *args, **kwargs):
        jwt_token = request.COOKIES.get('jwt_token')
        if not jwt_token:
            return HttpResponseBadRequest(status=403)

        current_user = verify_jwt_token(jwt_token)
        if current_user is None:
            return HttpResponseBadRequest(status=403)

        return view_func(request, current_user, *args, **kwargs)

    return wrapper





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



def login(request):
    if request.method == 'POST':

        form = UserForm(request.POST)
        if form.is_valid():
            # get user info from form
            username = form.cleaned_data['username']
        
            # create user object
            user = User(username=username, color = generate_random_color())
            user.save()
            # refresh fields
        
            data = {
                "user_id": user.id,
                "username": user.username
            }
            # generate jwt token
            token = generate_jwt_token(data)

            # Return token in json
            return JsonResponse({"token":token})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors})
        
    return HttpResponseBadRequest()





@requires_auth
def submit_message(request, current_user):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message_text = form.cleaned_data['message_text']
            message = Message(text=message_text, user=current_user)
            message.save()
            # TODO WEBSOCKET LOGINCS
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors})
    else:
        return HttpResponseBadRequest()
    