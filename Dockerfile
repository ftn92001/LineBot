FROM python:3
RUN mkdir -p /home/app
WORKDIR /home/app
COPY . /home/app
RUN pip install -r requirements.txt
CMD python manage.py runserver 0.0.0.0:$PORT