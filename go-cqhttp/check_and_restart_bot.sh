#!/bin/bash

# 指定BOt进程的名称和启动命令
BOT_PROCESS_NAME="go-cqhttp"

# 检查Bot进程是否存在
if pgrep -f "$BOT_PROCESS_NAME" > /dev/null ; then
    echo "Bot process $BOT_PROCESS_NAME is running."
else
    echo "Bot process $BOT_PROCESS_NAME is not running. Restarting..."
    # 重新启动Bot进程
    cd /root/go-cqhttp
    nohup /root/go-cqhttp/go-cqhttp &
fi
