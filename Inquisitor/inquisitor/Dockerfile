FROM python:3.9-slim-bookworm AS base

RUN apt-get update && \
    apt-get install -y libpcap-dev gcc iproute2 dsniff && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libpcap-dev # Install C libpcap development headers
RUN pip install python-libpcap 

RUN apt-get update && apt-get install -y arping

WORKDIR /app

COPY . .

CMD ["python", "inquisitor.py"] # Adjust 'inquisitor.py' if your main file has a different name