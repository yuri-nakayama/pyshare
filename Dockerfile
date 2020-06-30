FROM python:3.6.7

ENV PYTHONBUFFERED 1

RUN mkdir -p /var/www/flaskbasic
WORKDIR /var/www/flaskbasic

COPY requirements.txt /var/www/flaskbasic/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /var/www/flaskbasic/

# .は　allと言う意味
#  copyには毎回最後に / が必要