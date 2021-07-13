FROM python:3

WORKDIR /home/app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir -p uploads

COPY . .

CMD "python3" "app.py"