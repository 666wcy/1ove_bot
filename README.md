# final_bot

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)



添加Aria2NG,地址为https://xxxx.herokuapp.com/ng/

或者使用bot登录时发送的免输入登录网址，打开自动配置密码连接



修改主界面为 FolderMagic，账号为root，密码为aria2的密钥

https://github.com/FolderMagic/FolderMagic

webdav路径

https://xxxx.herokuapp.com/webdav,账号密码同上，不支持网页端，需要支持webdav的软件

探针路径

https://xxxx.herokuapp.com/status



~~修改主界面为filebrowser，用户名为root，密码为环境变量的aria2_secret~~ 

替换python flask为nginx，节省内存