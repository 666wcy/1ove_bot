FROM linuxserver/qbittorrent:version-14.2.5.99202004250119-7015-2c65b79ubuntu18.04.1

COPY root /


RUN chmod 0777 /rclone

RUN cp ./rclone /usr/bin/
RUN rm -rf /rclone

RUN chmod 777 /start.sh


#CMD tail -f /dev/null
#CMD yes "" | qbittorrent-nox --webui-port=$PORT --profile=/config 
CMD bash start.sh