FROM node:latest

WORKDIR /frontend
COPY . /frontend
RUN chown -R node:node /frontend

RUN npm install
EXPOSE 3000

CMD [ "node", "server.js" ]