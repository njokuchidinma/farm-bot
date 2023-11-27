FROM python:3.10-slim

ENV PYTHONBUFFERED=1

ADD ./requirements.txt /app/requirements.txt

ADD . /app 
WORKDIR /app

RUN apt update -y

RUN pip install --upgrade pip
RUN pip install django
RUN pip install djangorestframework
RUN pip install drf-yasg
RUN pip install django-filter==2.4.0
RUN pip install django-countries
RUN pip install requests
RUN pip install django-notifications-hq==1.7.0
RUN pip install openai
RUN pip install gunicorn

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--timeout", "600", "--workers", "1", "support.wsgi:application"]