FROM debian:bullseye

RUN apt update && apt install -y gcc libpcap-dev make iproute2 \
    iputils-ping python3 docker.io && rm -rf /var/lib/apt/lists/* 

COPY . /app

WORKDIR /app

# CMD ["python3", "inquisitor.py"]


# CMD ["sh"]

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]