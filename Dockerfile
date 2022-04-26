FROM python:3.7-slim
WORKDIR /var/www

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . ./

ENTRYPOINT pip3 install -r requirements.txt && python3 manage_dev.py makemigrations && python3 manage_dev.py migrate && python3 manage_dev.py runserver 0.0.0.0:8000