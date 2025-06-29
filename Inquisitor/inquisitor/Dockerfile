# inquisitor_project/your_inquisitor_program/Dockerfile
FROM python:3.9-slim-buster # Or any other suitable Python base image

# Install libpcap (required for sniffing even with Python libraries like scapy)
# And install python packages if needed (e.g. scapy)
RUN apt-get update && \
    apt-get install -y libpcap-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy your Python script
COPY . .

# Install Python dependencies (if you have a requirements.txt)
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# Default command (can be overridden by docker-compose)
CMD ["python", "inquisitor.py"] # Adjust 'inquisitor.py' if your main file has a different name