#!/usr/bin/python
# -*- coding: UTF-8 -*-
from subprocess import Popen, PIPE
import os
import json
import time
import datetime
import pytz
os.chdir(os.path.dirname(__file__))
with open('config.json', 'r', encoding='utf-8') as f:
    conf = json.loads(f.read())
    f.close()

tz = pytz.timezone('Asia/Shanghai') #东八区
#t = datetime.datetime.fromtimestamp(int(time.time()),tz).strftime('%Y年%m月%d日 %H:%M:%S')
upload_data = datetime.datetime.fromtimestamp(int(time.time()),tz).strftime('%Y年%m月%d日')

def start_upload_move(dir,folder,Remote,Upload):
    print(folder)
    dir=str(dir).replace("\\\\","\\")
    dir = dir.rstrip('\\')
    dir = dir.rstrip('/')

    folder=str(folder).replace("\\","/")
    folder=str(folder).replace("//","/")
    folder= folder.rstrip('\\')
    folder = folder.rstrip('\\')

    print(folder)
    if folder!="":
        print("上传判断，文件夹")
        command=f"rclone --config /config/rclone/rclone.conf move  \"{dir}\"  \"{Remote}:{Upload}/{upload_data}/{folder}\"  --stats=20s --stats-one-line --stats-log-level NOTICE "
        print(command)
        resultsCommond = Popen(command,stdout=PIPE,
                               stderr=PIPE,stdin=PIPE,shell=True)
        data = resultsCommond.stdout.read()
        return f"{Remote}:{Upload}/{upload_data}/{folder}"
    else:
        command=f"rclone --config /config/rclone/rclone.conf move  \"{dir}\"  \"{Remote}:{Upload}/{upload_data}\"  --stats=20s --stats-one-line --stats-log-level NOTICE  "
        resultsCommond = Popen(command,stdout=PIPE,
                               stderr=PIPE,stdin=PIPE,shell=True)
        data = resultsCommond.stdout.read()
        return f"{Remote}:{Upload}/{upload_data}"


def start_upload(dir,folder,Remote,Upload):
    print(folder)
    dir=str(dir).replace("\\\\","\\")
    dir = dir.rstrip('\\')
    dir = dir.rstrip('/')

    folder=str(folder).replace("\\","/")
    folder=str(folder).replace("//","/")
    folder= folder.rstrip('\\')
    folder = folder.rstrip('\\')
    print(folder)
    if folder!="":
        print("上传判断，文件夹")
        command=f"rclone --config /config/rclone/rclone.conf copy  \"{dir}\"  \"{Remote}:{Upload}/{upload_data}/{folder}\"  --stats=5s --stats-one-line --stats-log-level NOTICE "
        print(command)
        resultsCommond = Popen(command,stdout=PIPE,
                               stderr=PIPE,stdin=PIPE,shell=True)
        data = resultsCommond.stdout.read()
        return f"{Remote}:{Upload}/{upload_data}/{folder}"
    else:
        command=f"rclone --config /config/rclone/rclone.conf copy  \"{dir}\"  \"{Remote}:{Upload}/{upload_data}\"  --stats=5s --stats-one-line --stats-log-level NOTICE"
        print(command)
        resultsCommond = Popen(command,stdout=PIPE,
                               stderr=PIPE,stdin=PIPE,shell=True)
        data = resultsCommond.stdout.read()
        return f"{Remote}:{Upload}/{upload_data}"



if __name__ == '__main__':
    '''dir="D:\\BaiduNetdiskDownload\\xmind"
    start_upload(dir)'''
    print()

