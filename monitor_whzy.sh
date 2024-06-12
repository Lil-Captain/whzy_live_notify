#! /bin/bash

step=5

for ((i = 0; i < 60; i=(i+step))); do
    python /root/whzy_live_notify/whzy_live_notice.py
    python /root/whzy_live_notify/whzy_live_notice.py dev
    sleep $step
done
