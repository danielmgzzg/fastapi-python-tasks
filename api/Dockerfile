FROM python:3.9-slim AS builder
RUN apt-get -y update
RUN apt-get install -y  --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" 

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . .

CMD uvicorn tasks.main:app --reload --port $API_PORT --host 0.0.0.0 --log-level=info

FROM builder AS prod
COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$API_PORT tasks.main:app
