ARG PYTHON_VERSION=3.11.1
FROM python:${PYTHON_VERSION}

WORKDIR /code/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src ./src
