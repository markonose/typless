FROM python:3.10.8-slim-bullseye AS build

RUN pip install --upgrade pip

RUN groupadd -r -g 1000 bucket-consumer && useradd -r -g bucket-consumer -u 1000 bucket-consumer

# install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY *.py .

USER 1000
ENTRYPOINT [ "python", "main.py" ]
