FROM python:3.7-alpine

RUN pip install flask

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps


WORKDIR /home/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p uploads
RUN mkdir -p uploads/media
RUN mkdir -p uploads/templates
RUN mkdir -p uploads/photo
RUN mkdir -p uploads/tutorials
RUN mkdir -p reports

COPY . .

CMD "python3" "app.py"