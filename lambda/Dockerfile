FROM ubuntu:trusty

RUN apt-get -y update
RUN apt-get -y install wget apt-transport-https
RUN apt-get -y install python python-pip build-essential
RUN apt-get -y install python-dev
RUN pip install --upgrade pip
RUN pip install rethinkdb
RUN pip install tornado
RUN pip install requests
RUN apt-get -y install curl
#RUN pip install posix_ipc
RUN apt-get -y update
RUN apt-get -y install linux-tools-4.4.0-72-generic

COPY server.py /
COPY init /

CMD ["python", "/server.py"]
