# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

COPY . /app

COPY orders.csv /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV NAME World

CMD ["python", "-m", "unittest", "discover", "-s", "tests"]
