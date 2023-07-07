FROM python:3.9-alpine3.16

RUN python -m pip install --upgrade pip
COPY requirements.txt /temp/requirements.txt
COPY . /server
WORKDIR /server
EXPOSE 8000

# RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r /temp/requirements.txt

ENV PYTHONUNBUFFERED=1

RUN adduser --disabled-password server-user

USER server-user
