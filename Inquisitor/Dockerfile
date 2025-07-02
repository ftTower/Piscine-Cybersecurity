FROM debian:stable-slim

RUN apt-get update && \
    apt-get install -y vsftpd openssl && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/vsftpd/empty && \
    chown root:root /var/run/vsftpd/empty && \
    chmod 755 /var/run/vsftpd/empty

RUN useradd -m -s /bin/bash ftpuser

RUN echo "ftpuser:ftppassword" | chpasswd

COPY vsftpd.conf /etc/vsftpd.conf

RUN mkdir -p /home/ftpuser/ftp_data && \
    chown ftpuser:ftpuser /home/ftpuser/ftp_data

EXPOSE 20 21 21000-21010

CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]