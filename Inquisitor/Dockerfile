# Dockerfile for vsftpd server
FROM debian:stable-slim

# Install vsftpd and openssl
RUN apt-get update && \
    apt-get install -y vsftpd openssl && \
    rm -rf /var/lib/apt/lists/*

# --- ADD THESE LINES FOR secure_chroot_dir ---
RUN mkdir -p /var/run/vsftpd/empty && \
    chown root:root /var/run/vsftpd/empty && \
    chmod 755 /var/run/vsftpd/empty
# --- END ADDITION ---

# Create a user for FTP
RUN useradd -m -s /bin/bash ftpuser

# Set password for ftpuser (you can change this)
RUN echo "ftpuser:ftppassword" | chpasswd

# Configure vsftpd
COPY vsftpd.conf /etc/vsftpd.conf

# Create directory for FTP data and set permissions
RUN mkdir -p /home/ftpuser/ftp_data && \
    chown ftpuser:ftpuser /home/ftpuser/ftp_data

# Expose FTP control and passive ports
EXPOSE 20 21 21000-21010

# Start vsftpd
CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]