FROM python:latest


COPY . .
RUN pip install -r requirements.txt
WORKDIR /app
RUN python3 manage.py migrate

# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver"]