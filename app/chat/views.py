<<<<<<< HEAD
<<<<<<< HEAD
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
=======
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
    


    jwt_token = request.COOKIES.get('jwt_token', None)
    if jwt_token is None: current_user = None    
    else: current_user = verify_jwt_token(jwt_token)

    context = {
        'messages': messages, # Set array of messages to display
        'current_user': current_user
    }
    return render(request, 'chat_room.html', context)


def test_socket(request):
    return render(request, 'test_socket.html')


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
    
>>>>>>> 090aff871ce41a98081ffc8fa49023aefbb4e6e3
=======
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseNotAllowed
from .models import Message, User
from .lib import verify_jwt_token, generate_jwt_token, generate_random_color, generate_random_cat
from .base import find_message_by_id
from .forms import *
from .consumers import send_to_websocket_sync


def requires_auth(view_func): # Decorator to check for valid jwt token
    def wrapper(request, *args, **kwargs): 
        
        jwt_token = request.COOKIES.get('jwt_token')
        if not jwt_token:
            return HttpResponseBadRequest(content = "user unauthorized", status=403)

        current_user = verify_jwt_token(jwt_token)
        if current_user is None:
            return HttpResponseBadRequest(content = "user unauthorized", status=403)
        
        # If jwt_token is valid - pass current user to a function
        return view_func(request, current_user, *args, **kwargs)

    return wrapper


def requires_form(required_form): # Decorator to validate POST data 
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            # Validating form fields
            form = required_form(request.POST)
            if form.is_valid():
                return func(request, form.cleaned_data, *args, **kwargs) # Run the function
            else:
                # Returning an error if the field is not valid
                errors = form.errors.as_json()
                return JsonResponse({'errors': errors})
        return wrapper
    return decorator




def chat_room(request):
    messages = Message.objects.all()
    last_user = None
    # To hide all unnecessary avatars (duplicates)
    for message in reversed(messages):
        if message.user != last_user:
            last_user = message.user
            message.show_avatar = True
        else:
            message.show_avatar = False

    # Validating jwt token - current_user should be type(models.User) or None
    jwt_token = request.COOKIES.get('jwt_token', None)
    if jwt_token is None: current_user = None    
    else: current_user = verify_jwt_token(jwt_token)


    context = {
        'messages': messages, # Set array of messages to display
        'current_user': current_user
    }
    # Sending the template
    return render(request, 'chat_room.html', context)



@requires_form(UserForm) # Checks for form validity
def login(request, cleaned_data):
    if request.method == 'POST':

        # get username from form
        username = cleaned_data['username']

        # create user object
        catpic = generate_random_cat()
        user = User(username=username, color = generate_random_color(), avatar = catpic)
        user.save()
        # creating jwt_token data
        data = {
            "user_id": user.id,
            "username": user.username
        }
        # Creating jwt_token
        token = generate_jwt_token(data)

        # Return token in json
        return JsonResponse({"token":token, "user_id": user.id})
        
        
    return HttpResponseNotAllowed(["POST"])




@requires_auth # Checks wether the user is authorized
@requires_form(MessageForm) # Checks for form validity
@ratelimit(key='user', rate='45/m', block=True)
def submit_message(request, cleaned_data, current_user: User):

    if request.method == 'POST':
        message_text = cleaned_data['message_text']
        # Adding new message to database
        message = Message(text=message_text, user=current_user)
        message.save()
        # Creating websocket payload
        # django.forms.model_to_dict
        user = { 
            "id": message.user.id, 
            "username": message.user.username, 
            "user_color": message.user.color,
            'avatar': message.user.avatar
        }
        msg = { 
            "id": message.id, 
            "text": message_text, 
            "created": message.created_at.strftime("%B %d, %Y, %I:%M")
        } 
        # Sending data to websocket so it displays the message in real-time
        send_to_websocket_sync(type="send_message", message=msg, user=user)
        return JsonResponse({'success': True})
    else:
        return HttpResponseNotAllowed(["POST"])


@requires_auth
@requires_form(MessageForm)
def edit_message(request, cleaned_data, current_user: User, message_id):

    
    if request.method == 'POST':
        if not message_id: return HttpResponseBadRequest(content = 'not found', status=404)

        message = find_message_by_id(message_id)

        if message is None: # If message isn't in database
            return HttpResponseBadRequest(content = 'not found', status=404)

        if message.user != current_user: # If user is trying to edit someone else's message
            return HttpResponseBadRequest(content = 'unauthorized to perform this action', status=403)
        
        message.text = cleaned_data['message_text']

        message.edited = True
        message.save()
        
        data = { 
            "id": message.id, 
            "text": message.text
        } 
        send_to_websocket_sync(type="edit_message", message = data)
        return JsonResponse({"success": True})

    return HttpResponseNotAllowed(["POST"])
>>>>>>> origin/master
