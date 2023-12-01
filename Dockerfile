FROM python:3.13.0a1-bullseye

ENV PYTHONUNBUFFERED 1

RUN sudo apt-get update && sudo apt-get install -y libpq-dev

WORKDIR /app

COPY . /app/

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [ "sh", "-c", "python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000" ]