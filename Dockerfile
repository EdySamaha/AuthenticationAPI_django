FROM python:3.7.3
ENV PYTHONUNBUFFERED 1

WORKDIR /authentication
COPY requirements.txt /authentication/requirements.txt
RUN pip install -r requirements.txt
COPY . /authentication

# :8000 inside Docker container NOT our localhost. See docker-compose file
CMD python manage.py runserver 0.0.0.0:8000
