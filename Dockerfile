FROM alpine


COPY root /
RUN chmod 0777 /rclone

RUN cp ./rclone /usr/bin/
RUN rm -rf /rclone

RUN chmod 777 start.sh

RUN chmod 777 qbittorrent-nox
RUN mv qbittorrent-nox /usr/bin/
RUN apk add bash
#CMD tail -f /dev/null
#CMD yes "" | qbittorrent-nox --webui-port=$PORT --profile=/config 
CMD bash start.sh