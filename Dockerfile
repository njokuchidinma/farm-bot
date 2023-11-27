FROM python:3.10-slim

ENV PYTHONBUFFERED=1

ADD ./requirements.txt /app/requirements.txt

ADD . /app 
WORKDIR /app

RUN apt update -y

RUN pip install --upgrade pip
RUN pip install django
RUN pip install djangorestframework
RUN pip install -r /app/requirements.txt
RUN pip install gunicorn

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--timeout", "600", "--workers", "1", "support.wsgi:application"]