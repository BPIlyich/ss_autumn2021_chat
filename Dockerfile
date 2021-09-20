FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apt update
RUN apt install gettext -y
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /code/