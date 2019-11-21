# docker build -t ubuntu1604py36
FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git
RUN apt-get install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install --upgrade setuptools
RUN python3.6 -m pip install flask
RUN python3.6 -m pip install flask-restful
RUN python3.6 -m pip install gevent
RUN python3.6 -m pip install flasgger
RUN python3.6 -m pip install psycopg2

# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /root
#RUN mkdir conf
ADD . /root

VOLUME ["/root/conf"]

# Define default command.
ENTRYPOINT ["python3.6","/root/serverAPI.py"]
