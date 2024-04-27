FROM python:3.8-slim
WORKDIR /micro_service
COPY requirements.txt /micro_service
RUN pip3 install --upgrade pip -r requirements.txt
COPY . /micro_service
EXPOSE 5000