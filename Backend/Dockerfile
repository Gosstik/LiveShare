FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /app
COPY ./ /app
WORKDIR /app

# Creating user
RUN groupadd -g 1000 liveshare_admin_group && \
    useradd -u 1000 -g liveshare_admin_group -s /bin/bash -m liveshare_admin && \
    chown -R liveshare_admin:liveshare_admin_group /app
USER liveshare_admin

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
