FROM python3:11
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /Backend
COPY requirements.txt /.
COPY ./ ./
RUN pip install -r requirements.txt
EXPOSE 8000

# TODO
RUN python migrate
CMD python3 manage.py runserver 0.0.0.0:8000
