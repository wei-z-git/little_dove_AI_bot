#!/bin/bash

# 钉钉机器人的Webhook URL
WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=8f96245ccdecbab067dbb23807e787065c2cdfa53f2da9c73a182449538b3b39"

# 发送钉钉消息函数
send_dingding_message() {
    local message="$1"
    
    curl -H "Content-Type: application/json" \
         -X POST \
         -d "{\"msgtype\": \"text\", \"text\": {\"content\": \"$message\"}}" \
         "$WEBHOOK_URL"
}
