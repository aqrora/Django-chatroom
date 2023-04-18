# Django-chatroom

___

## Simple, chat-room on Django, Jquery, and Websockets, with the following features:

- Users can log in anonymously or by using username, login details are stored in JWT token
- Messages are stored in a database, and displayed via websocket
- Users can edit their own messages
- Rate limiting is implemented to prevent spamming

### Setup

`pip install -r requirements.txt`
`cd app`
`python3 manage.py migrate`

### Start app (windows cmd)
`start python manage.py runserver & start daphne --port 8001 app.asgi:application`

### Start app (bash)
`python3 manage.py runserver & daphne --port 8001 app.asgi:application`