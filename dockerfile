FROM python:3.8-alpine

COPY . /app

RUN pip3 install flask

WORKDIR /app

#port
ENV FLASK_RUN_PORT=8080

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]