FROM benchao/newubuntu:2.2



RUN mkdir /root/.aria2
COPY config /root/.aria2/

COPY root /

RUN pip3 install -r requirements.txt

#COPY bot /bot

RUN sudo chmod 777 /root/.aria2/
RUN sudo chmod 777 /rclone
RUN mv /rclone /usr/bin/

CMD wget https://github.com/666wcy/1ove_bot/raw/main/main  && chmod 0777 main && ./main