from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Message, User
from .lib import verify_jwt_token, generate_jwt_token




def requires_auth(view_func):
    def wrapper(request, *args, **kwargs):
        jwt_token = request.COOKIES.get('jwt_token')
        if not jwt_token:
            print("No jwt token")
            return HttpResponseBadRequest(status=403)

        current_user = verify_jwt_token(jwt_token)
        if current_user is None:
            return HttpResponseBadRequest(status=403)

        return view_func(request, current_user, *args, **kwargs)

    return wrapper






# @login_required
def chat_room(request):
    messages = Message.objects.all()
    jwt_token = request.COOKIES.get('jwt_token')
    show_popup = True
    # if jwt_token is not None and verify_jwt_token(jwt_token) is not None:
    #     show_popup = False

    context = {
        'show_popup': show_popup,  # Set this to True to show the popup
        'messages': messages # Set array of messages to display
    }
    return render(request, 'chat_room.html', context)



def login(request):
    if request.method == 'POST':
        # get user info from form
        username = request.POST['username']
        
        # create user object
        user = User(username=username)
        user.save()
        # refresh fields
        
        print(user.__dict__)
        data = {
            "user_id": user.id,
            "username": user.username
        }
        # generate jwt token
        token = generate_jwt_token(data)

        # Return token in json
        return JsonResponse({"token":token})
    
    return HttpResponseBadRequest()


@requires_auth
def submit_message(request, current_user):
    if request.method == 'POST':

        message_text = request.POST.get('message_text')
        message = Message(text=message_text, user=current_user)
        message.save()

        return HttpResponseRedirect('/')
    else:
        return HttpResponseBadRequest()
    