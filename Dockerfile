FROM alpine

COPY root /
RUN chmod 0777 /rclone

RUN cp ./rclone /usr/bin/
RUN rm -rf /rclone

RUN chmod 777 start.sh

chmod 777 qbittorrent-nox
mv qbittorrent-nox /usr/bin/

#CMD tail -f /dev/null
#CMD yes "" | qbittorrent-nox --webui-port=$PORT --profile=/config 
CMD bash start.sh