from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.http import JsonResponse
from .models import Message, User
from .lib import verify_jwt_token


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
        return render(request, 'error.html', {'error_message': 'Invalid request method.'})
    

def login(request):
    if request.method == 'POST':
        # get user info from form
        user_id = request.POST['user_id']
        username = request.POST['username']
        # create user object
        user = User(id=user_id, username=username)
        # login user and store user info in session
        auth.login(request, user)
        request.session['user_id'] = user_id
        request.session['username'] = username
        # redirect to success page
        return redirect('success')
    # render login page
    return render(request, 'login.html')