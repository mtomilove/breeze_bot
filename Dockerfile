FROM python:3.12

RUN apt-get update && apt-get install -y python3-distutils python3-apt

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "cli.py", "start", "api"]
