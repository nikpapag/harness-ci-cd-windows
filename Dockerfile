FROM python:3.9-windowsservercore-ltsc2022
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod -R 777 /app


CMD ["python3", "/app/main.py"]

