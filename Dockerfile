FROM benchao/qb:1.0


COPY root /

RUN chmod 0777 /rclone
RUN cp ./rclone /usr/bin/
RUN rm -rf /rclone

RUN sudo chmod 777 /start.sh

#CMD yes "" | qbittorrent-nox --webui-port=$PORT --profile=/config 
CMD bash start.sh