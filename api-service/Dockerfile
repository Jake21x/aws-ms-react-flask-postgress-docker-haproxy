FROM python:3

WORKDIR /home/app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./app.py .

CMD "python3" "app.py"