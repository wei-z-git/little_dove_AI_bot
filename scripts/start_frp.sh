#!/bin/bash
source $HOME/little_dove_ai_bot/scripts/send_dingding_message.sh
send_dingding_message "FRP service is starting!"

COMMAND="C:\Users\Administrator\Desktop\start-frp.bat.lnk"

ssh "administrator@192.168.28.205" "$COMMAND"