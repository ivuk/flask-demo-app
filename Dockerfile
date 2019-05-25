FROM python:3.6-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt && apk update && apk add curl

HEALTHCHECK CMD curl -sS --fail http://localhost:5000/ || exit 1

CMD ["python", "app.py"]
