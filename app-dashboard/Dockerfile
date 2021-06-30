FROM node:14-slim

WORKDIR /home/app

COPY ./package.json .
COPY ./yarn.lock .
COPY ./tsconfig.json .
COPY ./src ./src
COPY ./public ./public

RUN npm install

CMD npm start