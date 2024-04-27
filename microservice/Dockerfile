FROM python:3.8-slim
COPY requirements.txt /
RUN pip3 install --upgrade pip -r requirements.txt
WORKDIR /micro_service
# COPY . /micro_service
EXPOSE 5000