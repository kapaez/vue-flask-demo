FROM ubuntu

MAINTAINER oldgao
RUN apt-get update && apt-get install -y git
ADD requirement.txt requirement.txt
RUN apt-get install -y python-pip
RUN pip install -r requirement.txt
