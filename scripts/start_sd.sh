#!/bin/bash
source $HOME/little_dove_ai_bot/scripts/send_dingding_message.sh
send_dingding_message "SD service is starting!"
COMMAND="C:\Users\Administrator\Desktop\webui-user.bat.lnk"

ssh "administrator@192.168.28.205" "$COMMAND"
