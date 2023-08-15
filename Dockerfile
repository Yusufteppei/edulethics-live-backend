FROM python:3.9-alpine3.15

#   SET WORKDIR
WORKDIR /edulethics-exam-portal

#   SET ENV VARIABLES
ENV PYTHONBUFFERED = 1

#   INSTALL DEPENDENCIES
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#   COPY PROJECT

COPY . .

EXPOSE 8000

CMD gunicorn edulethics.wsgi:application --bind 0.0.0.0:8000