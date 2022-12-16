# Dockerfile 

FROM python:3.10-alpine

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

ENV FLASK_APP=app2
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_DEBUG=True

CMD ["flask", "run"]