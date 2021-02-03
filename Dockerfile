FROM ghcr.io/linuxserver/baseimage-ubuntu:bionic

RUN apt-get update
RUN apt-get install sudo
RUN sudo apt-get update

RUN sudo apt-get install software-properties-common -y

RUN sudo add-apt-repository ppa:qbittorrent-team/qbittorrent-stable -y

RUN sudo apt-get update
RUN sudo apt-get install qbittorrent-nox -y

RUN apt-get install vim-common -y

COPY root /


RUN chmod 0777 /rclone

RUN cp ./rclone /usr/bin/
RUN rm -rf /rclone
RUN sudo chmod 777 /start.sh


#CMD tail -f /dev/null
#CMD yes "" | qbittorrent-nox --webui-port=$PORT --profile=/config 
CMD bash start.sh