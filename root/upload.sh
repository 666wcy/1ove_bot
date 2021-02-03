#!/bin/sh
torrent_name=$1
content_dir=$2
root_dir=$3
save_dir=$4
files_num=$5
torrent_size=$6
file_hash=$7

DRIVE_NAME='${Remote}'   # 挂载盘名称
DRIVE_PATH='/upload'		#上传到盘的地址，后面没有 /
DOWNLOAD_PATH='/downloads/'		#qb下载默认地址

RETRY_NUM=3		#rclone上传重试次数

qb_version="4.2.5"  #qb版本
qb_username="admin"        #qb用户名
qb_password="adminadmin"        #qb密码
qb_web_url="http://localhost:8080"   #qb web地址
leeching_mode="true"  #true为自动删除上传的种子

auto_del_flag="rclone"   #上传完成后将种子标记的标签

tg_if="true"  #上传完成用Tg bot 进行通知，如果不开启下面两项不需要填,true为开启
chat_id="${Telegram_user_id}" #用户id，通过 @userinfobot 获取
bot_api="${Telegram_bot_api}" #自己申请的bot的API

#bash /upload/qb_auto.sh  "%N" "%F" "%R" "%D" "%C" "%Z" "%I"
echo "bash /upload/qb_auto.sh  ${torrent_name} ${content_dir} ${root_dir} ${save_dir} ${files_num} ${torrent_size} ${file_hash}"


version=$(echo $qb_version | grep -P -o "([0-9]\.){2}[0-9]" | sed s/\\.//g)


RED_FONT_PREFIX="\033[31m"
LIGHT_GREEN_FONT_PREFIX="\033[1;32m"
YELLOW_FONT_PREFIX="\033[1;33m"
LIGHT_PURPLE_FONT_PREFIX="\033[1;35m"
FONT_COLOR_SUFFIX="\033[0m"
INFO="[${LIGHT_GREEN_FONT_PREFIX}INFO]"
ERROR="[${RED_FONT_PREFIX}ERROR]"
WARRING="[${YELLOW_FONT_PREFIX}WARRING]"

DATE_TIME() {
    date +"%m/%d %H:%M:%S"
}



function UPLOAD_FILE() {
    echo -e "$(DATE_TIME) ${INFO} Start upload files..."
    
    RETRY=0
    while [ ${RETRY} -le ${RETRY_NUM} ]; do
        [ ${RETRY} != 0 ] && (
            echo
            echo -e "$(DATE_TIME) ${ERROR} Upload failed! Retry ${RETRY}/${RETRY_NUM} ..."
            
            echo
        )
        echo ${UPLOAD_PATH}
        echo ${REMOTE_PATH}
        rclone copy -v "${UPLOAD_PATH}" "${REMOTE_PATH}"
        RCLONE_EXIT_CODE=$?
        if [ ${RCLONE_EXIT_CODE} -eq 0 ]; then
            
            break
        else
            RETRY=$((${RETRY} + 1))
            [ ${RETRY} -gt ${RETRY_NUM} ] && (
                echo "$(DATE_TIME) ${ERROR} Upload failed: ${UPLOAD_PATH}" 
                
               
            )
            sleep 3
        fi
    done
}




function qb_login(){
	if [ ${version} -gt 404 ]
	then
		qb_v="1"
		cookie=$(curl -i --header "Referer: ${qb_web_url}" --data "username=${qb_username}&password=${qb_password}" "${qb_web_url}/api/v2/auth/login" | grep -P -o 'SID=\S{32}')
		if [ -n ${cookie} ]
		then
			echo "[$(date '+%Y-%m-%d %H:%M:%S')] 登录成功！cookie:${cookie}" 

		else
			echo "[$(date '+%Y-%m-%d %H:%M:%S')] 登录失败！"
		fi
	elif [[ ${version} -le 404 && ${version} -ge 320 ]]
	then
		qb_v="2"
		cookie=$(curl -i --header "Referer: ${qb_web_url}" --data "username=${qb_username}&password=${qb_password}" "${qb_web_url}/login" | grep -P -o 'SID=\S{32}')
		if [ -n ${cookie} ]
		then
			echo "[$(date '+%Y-%m-%d %H:%M:%S')] 登录成功！cookie:${cookie}" >> 
		else
			echo "[$(date '+%Y-%m-%d %H:%M:%S')] 登录失败" >> 
		fi
	elif [[ ${version} -ge 310 && ${version} -lt 320 ]]
	then
		qb_v="3"
		echo "陈年老版本，请及时升级"
		exit
	else
		qb_v="0"
		exit
	fi
}



function qb_del(){
	if [ ${leeching_mode} == "true" ]
	then
		if [ ${qb_v} == "1" ]
		then
			curl "${qb_web_url}/api/v2/torrents/delete?hashes=${file_hash}&deleteFiles=true" --cookie ${cookie}
			echo "[$(date '+%Y-%m-%d %H:%M:%S')] 删除成功！种子名称:${torrent_name}"
		elif [ ${qb_v} == "2" ]
		then
			curl -X POST -d "hashes=${file_hash}" "${qb_web_url}/command/deletePerm" --cookie ${cookie}
		else
			echo "[$(date '+%Y-%m-%d %H:%M:%S')] 删除成功！种子文件:${torrent_name}"
			echo "qb_v=${qb_v}"
		fi
	else
		echo "[$(date '+%Y-%m-%d %H:%M:%S')] 不自动删除已上传种子"
	fi
}


function qb_add_auto_del_tags(){
	if [ ${qb_v} == "1" ]
	then
		curl -X POST -d "hashes=${file_hash}&tags=${auto_del_flag}" "${qb_web_url}/api/v2/torrents/addTags" --cookie "${cookie}"
	elif [ ${qb_v} == "2" ]
	then
		curl -X POST -d "hashes=${file_hash}&category=${auto_del_flag}" "${qb_web_url}/command/setCategory" --cookie ${cookie}
	else
		echo "qb_v=${qb_v}"
	fi
}

echo ${content_dir}
if [ -f "${content_dir}" ]
then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 类型：文件"
   
   type="file"
   
    
    
    RELATIVE_PATH=${content_dir#${DOWNLOAD_PATH}}  #文件夹名称
    
    echo $RELATIVE_PATH
    NEW_PATH=${RELATIVE_PATH%%/*}
    echo $NEW_PATH
    UPLOAD_PATH="${content_dir}"
    REMOTE_PATH="${DRIVE_NAME}:${DRIVE_PATH}/${NEW_PATH}"
    echo $UPLOAD_PATH
    echo $REMOTE_PATH
   UPLOAD_FILE
   qb_login
   qb_add_auto_del_tags
   qb_del
elif [ -d "${content_dir}" ]
then 
   echo "[$(date '+%Y-%m-%d %H:%M:%S')] 类型：目录"
   type="dir"
   RELATIVE_PATH=${content_dir#${DOWNLOAD_PATH}}  #文件夹名称
    
    echo $RELATIVE_PATH
    UPLOAD_PATH="${content_dir}"
    REMOTE_PATH="${DRIVE_NAME}:${DRIVE_PATH}/${RELATIVE_PATH}"

    echo $UPLOAD_PATH
    echo $REMOTE_PATH
   UPLOAD_FILE
   qb_login
   qb_add_auto_del_tags
   qb_del
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 未知类型，取消上传"
fi

echo "种子名称：${torrent_name}"
echo "内容路径：${content_dir}"
echo "根目录：${root_dir}"
echo "保存路径：${save_dir}"
echo "文件数：${files_num}"
echo "文件大小：${torrent_size}Bytes"
echo "HASH:${file_hash}"
echo "上传地址:${REMOTE_PATH}"
#echo "Cookie:${cookie}"
echo -e "-------------------------------------------------------------\n"
if [ ${tg_if} == "true" ]
then

send_text=`echo -ne "种子名称：${torrent_name}\n内容路径：${content_dir}\n根目录：${root_dir}\n保存路径：${save_dir}\n文件数：${files_num}\n文件大小：${torrent_size}Bytes\nHASH:${file_hash}\n上传地址:${DRIVE_NAME}" | xxd -plain | tr -d '\n' | sed 's/\(..\)/%\1/g'`


curl GET "https://api.telegram.org/bot${bot_api}/sendMessage?chat_id=${chat_id}&text=${send_text}"
fi