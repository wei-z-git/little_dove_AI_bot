#!/bin/bash
source $HOME/little_dove_ai_bot/scripts/send_dingding_message.sh
COMMAND="shutdown -s -t 60"

ssh "administrator@192.168.28.205" "$COMMAND"

send_dingding_message "Shutdown message sent!"