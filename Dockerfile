FROM python:3.10-alpine
RUN mkdir -p /home/app
WORKDIR /home/app
COPY . /home/app
RUN apk add \
    wget \
    gcc \
    make \
    zlib-dev \
    libffi-dev \
    openssl-dev \
    musl-dev
RUN pip install -r requirements.txt
CMD python manage.py runserver 0.0.0.0:8000
