#!/usr/bin/env bash
chmod 0777 /upload/ -R
python3 /upload/config.py
yes "" | qbittorrent-nox --webui-port=$PORT --profile=/config