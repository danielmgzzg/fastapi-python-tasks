FROM python:3.9-slim AS builder
RUN apt-get -y update
RUN apt-get install -y  --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" 

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . .

FROM builder AS prod

ENV PATH="/opt/venv/bin:$PATH"
CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$API_PORT tasks.main:app
