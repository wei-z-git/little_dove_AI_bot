# little_dove_ai_bot

[![release tag](https://img.shields.io/gitlab/v/release/wei-z-git/little_dove_ai_bot?gitlab_url=https%3A%2F%2Fjihulab.com&include_prereleases&sort=semver)](https://jihulab.com/wei-z-git/little_dove_ai_bot/-/releases)
[![build status](https://img.shields.io/gitlab/pipeline-status/wei-z-git/little_dove_ai_bot?branch=main&gitlab_url=https%3A%2F%2Fjihulab.com%2F)](https://jihulab.com/wei-z-git/little_dove_ai_bot/-/pipelines)

## 1.How to start

### Deploy to local

```
python3 bot.py
```

### Docker

```
docker run -d --name little_dove_ai_bot_{{tag}} \
-e HOST="0.0.0.0" \
-e PORT="80" \
-e GOCQ_ACCOUNTS='[{ "uin": "","protocol":2}]' \
-e SUPERUSERS='["", "superadmin"]' \
-e NICKNAME='["dove_ai", "bot"]' \
-e COMMAND_START='[""]' \
-e FORWARDER_SOURCE_GROUP='[""]' \
-e FORWARDER_DEST_GROUP='[""]' \
-e FORWARDER_PREFIX='[""]' \
-e FORWARDER_EXPLICT='["",""]' \
-e wordcloud_exclude_user_ids="[2838376057]" \
-e FORWARDER_SHOW_SENDER="card" \
-e WORDCLOUD_TIMEZONE="Asia/Shanghai" \
-v /tmp/accounts:/app/accounts \
-v /tmp/data:/app/data \
-v /tmp/nonebot2:/root/.local/share/nonebot2 \
-p {{port}}:80 \
registry.jihulab.com/wei-z-git/little_dove_ai_bot:{{tag}}
```

2. scan QR-code to login

## 2.Nonebot Documentation

See [Docs](https://v2.nonebot.dev/)
GPT3-plugin: https://github.com/chrisyy2003/nonebot-plugin-gpt3
CHATGPT-plugin: https://github.com/A-kirami/nonebot-plugin-chatgpt

# Developer

### TODO:

#### Stable diffusion

- [ ] Build stable ui docker image
- [ ] Nonebot2 plugin of Stable diffusion
- [ ]

#### Mockingbird

- [ ] mockingbird 插件？

#### Others

- [ ] nonebot-plugin-forwarder 加后缀
- [X] 加入ac机器人自动回复
- [X] 调查maskpng无法被加载原因
- [X] 尝试临时简单加入切换maskpng图片的功能（在作者添加此功能之前）
- [X] 整理词云readme, 需要maskpng先被正常加载

#### qq-group-message-summary

- [X] 接入~~文心一言~~ llama3
- [X] 过滤测试指令（关键词）
- [X] 消息切割（2000字符）
- [ ] 定时发送
- [ ] 指令/显示消息长度
- [ ] 指令/修改prompt
- [ ] 指令/详尽模式: 更加详细的总结
- [ ] get_message可以指定排除用户id，不需要额外过滤方法
- [ ] 通过get_message指定群

---

### Completed

- [X] Init
- [X] 查看群活跃度
- [X] 查看群活跃度并进行性别筛选

- ~~将不活跃群员加入冷库~~ - 无法实现

- [X] 从原有群踢出
