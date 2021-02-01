#!/usr/bin/python
# -*- coding: UTF-8 -*-
import qbittorrentapi
import time
import json
import telebot
with open('/upload/config.json', 'r', encoding='utf-8') as f:
    conf = json.loads(f.read())
    f.close()
QB_host=conf["QB_host"]
QB_port=conf["QB_port"]
QB_username=conf["QB_username"]
QB_password=conf["QB_password"]
Telegram_bot_api=conf["Telegram_bot_api"]
Telegram_user_id=conf["Telegram_user_id"]
qbt_client = qbittorrentapi.Client(host=QB_host, port=QB_port, username=QB_username, password=QB_password)
bot = telebot.TeleBot(Telegram_bot_api)
BOT_name=bot.get_me().username
print(BOT_name)
bot.send_message(chat_id=Telegram_user_id,text="bot已上线")
try:
    qbt_client.auth_log_in()
    print("ssuccess!!! qb连接成功，配置正确")

except qbittorrentapi.LoginFailed as e:
    print(f"error!!! qb配置不正确，请检查配置,错误信息：{e}")

except:
    print(f"error!!! qb配置不正确，请检查配置")

def cal_time(upload_time):
    m, s = divmod(int(upload_time), 60)
    h, m = divmod(m, 60)
    print ("%02d时%02d分%02d秒" % (h, m, s))
    if h !=0 :
        last_time="%d时%d分%d秒" % (h, m, s)
    elif h==0 and m!=0:
        last_time="%d分%d秒" % ( m, s)
    else:
        last_time="%d秒" % s
    return last_time

def hum_convert(value):
    value=float(value)
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size

#查看种子状态
'''    for torrent in qbt_client.torrents_info():
        print(torrent)
        print(hum_convert(torrent.total_size))
        print(f'{torrent.hash}: {torrent.name} ({torrent.state})')'''

#下载种子
#qbt_client.torrents_add(urls="magnet:?xt=urn:btih:LYY6IFQMU74Z3IZU4SHKDO6NU4M6G54P&dn=&tr=http%3A%2F%2F104.238.198.186%3A8000%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker3.itzmx.com%3A6961%2Fannounce&tr=http%3A%2F%2Ftracker4.itzmx.com%3A2710%2Fannounce&tr=http%3A%2F%2Ftracker.publicbt.com%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.prq.to%2Fannounce&tr=http%3A%2F%2Fopen.acgtracker.com%3A1096%2Fannounce&tr=https%3A%2F%2Ft-115.rhcloud.com%2Fonly_for_ylbud&tr=http%3A%2F%2Ftracker1.itzmx.com%3A8080%2Fannounce&tr=http%3A%2F%2Ftracker2.itzmx.com%3A6961%2Fannounce&tr=udp%3A%2F%2Ftracker1.itzmx.com%3A8080%2Fannounce&tr=udp%3A%2F%2Ftracker2.itzmx.com%3A6961%2Fannounce&tr=udp%3A%2F%2Ftracker3.itzmx.com%3A6961%2Fannounce&tr=udp%3A%2F%2Ftracker4.itzmx.com%3A2710%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce")

#downloading

#获取全部种子信息
def get_all_status():
    torrent_temp = qbt_client.torrents_info()

    if torrent_temp==[]:
        return ""
    the_info=[]
    for torrent in torrent_temp:
        print(torrent)
        print(hum_convert(torrent.completed))
        print(hum_convert(torrent.total_size))
        #percentage=float(torrent.completed)/float(torrent.total_size)
        percentage='{:.2f}%'.format(float(torrent.completed)/float(torrent.total_size)*100)

        data=10
        a=int((float(torrent.completed)/float(torrent.total_size)*10))
        d = '■' * a
        b = '□' * ( data- a)
        c = (a / data) * 100

        print(f'{torrent.hash}: {torrent.name} ({torrent.state})')
        print(torrent.time_active)

        the_info_temp=f"种子名称:`{torrent.name}`\n" \
                 f"种子状态:`{torrent.state}`\n" \
                 f"种子大小:`{hum_convert(torrent.total_size)}`\n" \
                 f"做种人数:`{torrent.num_complete}`\n" \
                  f'下载进度:`[{d}{b}]{percentage} `\n' \
                  f"下载速度:`{hum_convert(torrent.dlspeed)}`\n" \
                 f"下载用时:`{cal_time(torrent.time_active)}`\n" \
                 f"种子hash:`{torrent.hash}`"
        the_info.append(the_info_temp)


    return the_info

def get_solo_status(the_hash):
    torrent_temp = qbt_client.torrents_info(hashes=the_hash)

    if torrent_temp==[]:
        return ""
    torrent=torrent_temp[0]
    percentage='{:.2f}%'.format(float(torrent.completed)/float(torrent.total_size)*100)

    data=10
    a=int((float(torrent.completed)/float(torrent.total_size)*10))
    d = '■' * a
    b = '□' * ( data- a)
    c = (a / data) * 100

    print(f'{torrent.hash}: {torrent.name} ({torrent.state})')
    print(torrent.time_active)

    the_info=f"种子名称:`{torrent.name}`\n" \
              f"种子状态:`{torrent.state}`\n" \
              f"种子大小:`{hum_convert(torrent.total_size)}`\n" \
             f"做种人数:`{torrent.num_complete}`\n" \
             f'下载进度:`[{d}{b}]{percentage} `\n' \
              f"下载速度:`{hum_convert(torrent.dlspeed)}`\n" \
              f"下载用时:`{cal_time(torrent.time_active)}`\n" \
              f"种子hash:`{torrent.hash}`\n\n"

    the_info=the_info+f"剩余空间:`{hum_convert(qbt_client.sync_maindata().server_state.free_space_on_disk)}`"
    print(the_info)
    return the_info

def download_torrent(url):
    result=qbt_client.torrents_add(urls=url)
    print(result)
    if result=="Fails.":
        print("添加任务失败")
        return "添加任务失败,请检查磁力格式"
    elif result=="Ok.":
        print("添加任务成功")
        return "添加任务成功"

def del_torrent(hash):
    # instantiate a Client using the appropriate WebUI configuration
    qbt_client.torrents_delete(delete_files=True,torrent_hashes=hash)
    return "已发送请求，请检查状态"

def start_torrent(hash):
    qbt_client.torrents_resume(torrent_hashes=hash)
    return "已发送请求，请检查状态"

def pause_torrent(hash):
    qbt_client.torrents_pause(torrent_hashes=hash)
    return "已发送请求，请检查状态"

@bot.message_handler(commands=['status'])
def start_status(message):
    try:
        keywords = str(message.text)
        if keywords==f"/status@{BOT_name}":
            result_list=get_all_status()
            id_list=[]
            for result in result_list:
                id_temp=bot.send_message(chat_id=message.chat.id,text=result,parse_mode='Markdown').message_id
                print(id_temp)
                id_list.append(id_temp)
            text=f"剩余空间:`{hum_convert(qbt_client.sync_maindata().server_state.free_space_on_disk)}`"
            id_temp=bot.send_message(chat_id=message.chat.id,text=text,parse_mode='Markdown').message_id
            id_list.append(id_temp)
            time.sleep(20)
            for message_id in id_list:
                bot.delete_message(chat_id=message.chat.id,message_id=message_id)

        elif str(BOT_name) in keywords:
            # print(message.chat.type)
            keywords = keywords.replace(f"/status@{BOT_name} ", "")
            print(keywords)
            result=get_solo_status(keywords)
            bot.send_message(chat_id=message.chat.id,text=result,parse_mode='Markdown')

        elif keywords==f"/status":
            result_list=get_all_status()
            id_list=[]
            for result in result_list:
                id_temp=bot.send_message(chat_id=message.chat.id,text=result,parse_mode='Markdown').message_id
                print(id_temp)
                id_list.append(id_temp)
            text=f"剩余空间:`{hum_convert(qbt_client.sync_maindata().server_state.free_space_on_disk)}`"
            id_temp=bot.send_message(chat_id=message.chat.id,text=text,parse_mode='Markdown').message_id
            id_list.append(id_temp)
            time.sleep(20)
            for message_id in id_list:
                bot.delete_message(chat_id=message.chat.id,message_id=message_id)
        else:
            keywords = keywords.replace(f"/status ", "")
            print(keywords)
            result=get_solo_status(keywords)
            bot.send_message(chat_id=message.chat.id,text=result,parse_mode='Markdown')
    except:
        print("status函数报错")

@bot.message_handler(commands=['down'],func=lambda message:str(message.chat.id) == str(Telegram_user_id))
def start_download(message):
    try:
        keywords = str(message.text)
        if str(BOT_name) in keywords:
            keywords = keywords.replace(f"/down@{BOT_name} ", "")
            print(keywords)
            result=download_torrent(keywords)
            bot.send_message(chat_id=Telegram_user_id,text=result)
        else:
            keywords = keywords.replace(f"/down ", "")
            print(keywords)
            result=download_torrent(keywords)
            bot.send_message(chat_id=Telegram_user_id,text=result)

    except:
        print("down函数错误")

@bot.message_handler(commands=['resume'],func=lambda message:str(message.chat.id) == str(Telegram_user_id))
def start_start(message):
    try:
        keywords = str(message.text)
        if str(BOT_name) in keywords:
            keywords = keywords.replace(f"/resume@{BOT_name} ", "")
            print(keywords)
            result=start_torrent(keywords)
            bot.send_message(chat_id=Telegram_user_id,text=result)
        else:
            keywords = keywords.replace(f"/resume ", "")
            print(keywords)
            result=start_torrent(keywords)
            bot.send_message(chat_id=Telegram_user_id,text=result)
    except:
        print("resume函数错误")

@bot.message_handler(commands=['pause'],func=lambda message:str(message.chat.id) == str(Telegram_user_id))
def start_start(message):
    try:
        keywords = str(message.text)
        if str(BOT_name) in keywords:
            keywords = keywords.replace(f"/pause@{BOT_name} ", "")
            print(keywords)
            result=pause_torrent(keywords)
            bot.send_message(chat_id=Telegram_user_id,text=result)
        else:
            keywords = keywords.replace(f"/pause ", "")
            print(keywords)
            result=pause_torrent(keywords)
            bot.send_message(chat_id=Telegram_user_id,text=result)
    except:
        print("pause函数错误")


@bot.message_handler(commands=['del'],func=lambda message:str(message.chat.id) == str(Telegram_user_id))
def start_start(message):
    try:
        keywords = str(message.text)
        if str(BOT_name) in keywords:
            keywords = keywords.replace(f"/del@{BOT_name} ", "")
            print(keywords)
            result=del_torrent(keywords)
            bot.send_message(chat_id=Telegram_user_id,text=result)
        else:
            keywords = keywords.replace(f"/del ", "")
            print(keywords)
            result=del_torrent(keywords)
            bot.send_message(chat_id=Telegram_user_id,text=result)
    except:
        print("del函数错误")

@bot.message_handler(commands=['help'])
def start_start(message):
    try:
        text='''/status 查看所有种子状态
/status hash 查看对应hash的种子状态
/down 磁力链接 下载种子
/resume hash 继续种子任务
/pause hash 暂停种子任务
/del hash 删除种子
    '''
        bot.send_message(chat_id=message.chat.id,text=text)
    except:
        print("help函数出错")

if __name__ == '__main__':
    bot.enable_save_next_step_handlers(delay=2)

    # Load next_step_handlers from save file (default "./.handlers-saves/step.save")
    # WARNING It will work only if enable_save_next_step_handlers was called!
    bot.load_next_step_handlers()
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)







