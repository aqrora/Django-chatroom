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