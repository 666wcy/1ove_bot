# -*- coding: UTF-8 -*-
import json
import os
os.chdir(os.path.dirname(__file__))
QB_port=os.environ.get('PORT')
Telegram_bot_api=os.environ.get('Telegram_bot_api')
Telegram_user_id=os.environ.get('Telegram_user_id')
Rule=os.environ.get('Rule')
Rule=Rule.split("\n")

rclone=os.environ.get('rclone')

def mkdir(path):
    # 引入模块
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        os.makedirs(path)
        print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False


print(f"Telegram_bot_api:{Telegram_bot_api}\n"
      f"Telegram_user_id:{Telegram_user_id}\n"
      f"QB_port:{QB_port}\n"
      f"Rule:{Rule}"
      f"rclone:{rclone}")

mkdir("/config/rclone")
with open("/config/rclone/rclone.conf", "w") as f:
    f.write(rclone)
    f.close()

with open("/upload/config.json", "r",encoding='utf-8') as jsonFile:
    data = json.load(jsonFile)
    jsonFile.close()

data["QB_port"] = QB_port
data["Telegram_bot_api"] = Telegram_bot_api
data["Telegram_user_id"] = Telegram_user_id

new_rule=[]
for a in  Rule:
    new_rule.append(json.loads(a))
data["Rule"] = new_rule


with open("/upload/config.json", "w") as jsonFile:
    json.dump(data, jsonFile,ensure_ascii=False)
    jsonFile.close()