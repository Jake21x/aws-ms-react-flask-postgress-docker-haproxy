FROM python:3

WORKDIR /home/app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir -p uploads
RUN mkdir -p uploads/media
RUN mkdir -p uploads/templates
RUN mkdir -p uploads/photo
RUN mkdir -p uploads/tutorials

COPY . .

CMD "python3" "app.py"