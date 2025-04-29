FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /app
COPY ./ /app
WORKDIR /app

# TODO: create user ???

RUN pip install -r requirements.txt

CMD python3 manage.py runserver 0.0.0.0:8000

EXPOSE 8000
