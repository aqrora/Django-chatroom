<<<<<<< HEAD
 
=======
FROM python:latest



COPY . .
RUN pip install -r requirements.txt
WORKDIR /app
RUN python3 manage.py migrate
# RUN set DAPHNE_PORT=${DAPHNE_PORT} && set APP_PORT=${APP_PORT}
RUN chmod +x entrypoint.sh 
EXPOSE 8000
# CMD ./entrypoint.sh
>>>>>>> origin/master
