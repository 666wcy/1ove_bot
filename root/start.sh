#!/usr/bin/env bash

mkdir  /root/.config/rclone/
echo "${rclone}" >> /root/.config/rclone/rclone.conf
ulimit -m 314400
ulimit -v 314400
/usr/bin/qbittorrent-nox --webui-port=$PORT
#nohup yes "" | qbittorrent-nox --webui-port=$PORT --profile=/config &