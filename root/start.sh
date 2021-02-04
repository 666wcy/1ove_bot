#!/bin/bash

#mkdir  /root/.config/rclone/
#echo "${rclone}" >> /root/.config/rclone/rclone.conf
yes "" | qbittorrent-nox --webui-port=$PORT
#nohup yes "" | qbittorrent-nox --webui-port=$PORT --profile=/config &