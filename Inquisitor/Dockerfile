FROM python:3.11-slim

RUN apt-get update && apt-get install -y tcpdump iproute2 libpcap-dev net-tools && \
    pip install --no-cache-dir scapy

WORKDIR /app
COPY inquisitor.py /app/inquisitor.py

CMD ["tail", "-f", "/dev/null"]
