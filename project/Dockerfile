# pull official base image
FROM python:3.11.2-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc curl wget\
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy app
COPY . .

# instalamos el certificado de la ses
# COPY app/soporte/PRE_SGSICS.SES.MIR.ES.cer /usr/local/share/ca-certificates/
# RUN update-ca-certificates

CMD ["/bin/bash"]