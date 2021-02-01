#!/usr/bin/env bash
chmod 0777 /upload/ -R
python3 /upload/config.py
nohup yes "" | qbittorrent-nox --webui-port=$PORT --profile=/config &
python3 /upload/bot.py