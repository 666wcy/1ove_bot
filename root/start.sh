#!/usr/bin/env bash
chmod 0777 /upload.sh
echo "${rclone}" >> /.config/rclone/rclone.conf
yes "" | qbittorrent-nox --webui-port=$PORT --profile=/config