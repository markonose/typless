FROM python:3.10.8-slim-bullseye AS build

RUN pip install --upgrade pip

RUN groupadd -r -g 1000 api && useradd -r -g api -u 1000 api

# install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app /app

USER 1000

EXPOSE 5000
ENTRYPOINT [ "uvicorn", "app.main:app", "--workers", "1", "--host", "0.0.0.0", "--port", "5000" ]
