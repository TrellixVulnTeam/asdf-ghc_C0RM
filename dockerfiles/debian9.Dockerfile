FROM debian:9

RUN apt-get update && \
    apt-get install -y \
      build-essential \
      ca-certificates \
      lsb-release \
      python3

COPY . /root/project

WORKDIR /root/project

RUN /usr/bin/python3 --version
RUN /usr/bin/python3 -m unittest
