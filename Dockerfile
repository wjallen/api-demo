FROM python:3.12

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r ./requirements.txt

COPY src/api.py src/worker.py src/jobs.py ./
