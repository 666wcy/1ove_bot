#!/usr/bin/env bash
chmod 0777 upload.sh
mkdir  /root/.config/rclone/
echo "${rclone}" >> /root/.config/rclone/rclone.conf

#nohup yes "" | qbittorrent-nox --webui-port=$PORT --profile=/config &