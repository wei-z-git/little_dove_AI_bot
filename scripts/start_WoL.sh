#!/bin/bash
source "$HOME/little_dove_AI_bot/scripts/send_dingding_message.sh"
for i in {1..10}
do
    "$HOME/little_dove_AI_bot/scripts/WoL.sh" 04:7C:16:7B:0E:0D 192.168.28.205
done
send_dingding_message "WOL message sent!"