```shell
docker run -d --name onebot-docker0 -e VNC_PASSWD=vncpasswd -p 3000:3000 -p 6099:6099 -p 3001:3001 -v ${PWD}/LiteLoader:/opt/QQ/resources/app/LiteLoader mlikiowa/llonebot-docker:latest
```

然后浏览器访问 `http://你的docker-ip:6099/api/panel/getQQLoginQRcode` 扫码登录

登录之后访问 `http://你的docker-ip:6099/plugin/LLOneBot/iframe.html` 进行 llonebot 的配置



napcat 


```
docker run -d \
-e ACCOUNT=<机器人qq> \
-e WS_ENABLE=true \
-p 3001:3001 \
-p 6099:6099 \
--name napcat \
--restart=always \
mlikiowa/napcat-docker:latest
```



`http://$host:$port$prefix/webui/login.html`
