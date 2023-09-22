FROM python:3.8-slim
COPY *.py /
RUN apt-get update
COPY template.html /
COPY feedback.html /
COPY requirements.txt /
RUN pip3 install -r requirements.txt
