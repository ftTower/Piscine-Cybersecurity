FROM debian:bullseye

RUN apt update && apt install -y gcc libpcap-dev make iproute2 \
    iputils-ping python3 && rm -rf /var/lib/apt/lists/* 

COPY . /app
WORKDIR /app

RUN make

CMD [ "python3", "inquisitor.py" ]