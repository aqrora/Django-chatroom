# Django-chatroom

___

## Simple, chat-room on Django, Jquery, and Websockets, with the following features:

- Users can log in anonymously or by using username, login details are stored in JWT token
- Messages are stored in a database, and displayed via websocket
- Users can edit their own messages
- Rate limiting is implemented to prevent spamming

## Setup

`pip install -r requirements.txt`

`cd app`

`python3 manage.py migrate`

___
### Start app (windows cmd)
`start python manage.py runserver & start daphne --port 8001 app.asgi:application`

### Start app (bash)
`python3 manage.py runserver & daphne --port 8001 app.asgi:application`
___

# Preview: 

## Login screen
![Login Screen](https://user-images.githubusercontent.com/123666851/236958616-88617fc4-88c0-4135-82db-0f3becee3a6d.png)
## Chatroom itself (from 2 users)
![Messages Preview](https://user-images.githubusercontent.com/123666851/236958617-3f90baf5-dc45-4c9c-9d8e-c01272c2621a.png)
## Edit messages
![Edit Message](https://user-images.githubusercontent.com/123666851/236958619-94f7d383-16e9-44e8-9d6f-5eb38d572799.png)
## Hover to see details
![Message details](https://user-images.githubusercontent.com/123666851/236959328-ff578493-7349-4981-8a7d-079b5c406f7d.png)
