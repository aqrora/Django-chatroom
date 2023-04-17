#!/bin/bash

python3 manage.py runserver 0.0.0.0:8000 & 
daphne --port 8001 app.asgi:application  