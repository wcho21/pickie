FROM python:3.13.2-bookworm

RUN apt-get update && \
    apt-get install gnupg2=2.2.40-1.1 -y && \
    apt-get install vim=2:9.0.1378-2+deb12u2 -y && \
    rm -rf /var/lib/apt/lists/*