FROM ghcr.io/linuxserver/baseimage-ubuntu:bionic

RUN apt-get update
RUN apt-get install sudo
RUN sudo apt-get update

RUN sudo apt-get install software-properties-common -y

RUN sudo add-apt-repository ppa:qbittorrent-team/qbittorrent-stable -y

RUN sudo apt-get update
RUN sudo apt-get install qbittorrent-nox -y

RUN apt-get install yum -y
RUN apt-get install wget -y

RUN sudo apt-get install expect -y

RUN wget https://bootstrap.pypa.io/get-pip.py

RUN sudo apt-get install python3-distutils -y
RUN python3 get-pip.py

RUN pip3 install pyTelegramBotAPI
RUN pip3 install qbittorrent-api

RUN sudo apt-get install cron -y

RUN sudo /usr/sbin/service cron start 

RUN sudo apt install vim -y 

RUN sudo apt-get install git -y

COPY root /
RUN mkdir /upload
COPY upload /upload

RUN chmod 0777 /rclone

RUN cp ./rclone /usr/bin/
RUN rm -rf /rclone
RUN sudo chmod 777 /upload/ -R
RUN sudo chmod 777 /start.sh

RUN chmod 0777 /upload/ -R
#CMD tail -f /dev/null
#CMD yes "" | qbittorrent-nox --webui-port=$PORT --profile=/config 
CMD bash start.sh