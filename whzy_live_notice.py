import requests
import pdb
import sys
import json
from datetime import datetime
import os
# from pycqBot.cqCode import image

def image(file):
    return f"[CQ:image,file={file}]"

def get_bili_live_msg(uids):
    url = "https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids"
    json_data = json.dumps({"uids": uids})
    headers = {'Content-Type': 'application/json','Cookie': 'LIVE_BUVID=AUTO9216783447652998', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.request("POST", url, headers=headers, data=json_data)
    return response

def send_to_qq(msg, group_ids):
    for group_id in group_ids:
        url = "http://127.0.0.1:8000/send_msg"#这里要加上http://，不然会报错
        params = {
            "message_type": 'message',
            "group_id": group_id,
            "message": msg
        }
        requests.get(url,params=params)

def set_live_message(liveData):
        """
        开播消息格式
        """
        return "%s开播了！\n%s\n直播分区：%s\n====================\n%s\n%s" % (
            liveData["uname"],
            liveData["title"],
            "%s-%s-%s" % (
                liveData["area_name"], 
                liveData["area_v2_parent_name"], 
                liveData["area_v2_name"]
            ),
            image(liveData["cover_from_user"]),
            "https://live.bilibili.com/%s" % liveData["room_id"],
        )
    
def set_live_end_message(liveData):
    """
    下播消息格式
    """
    # cover_file_name = liveData["cover_from_user"].split("/")[-1]
    return "%s下播了...\n%s\n直播分区：%s\n====================\n%s\n%s" % (
        liveData["uname"],
        liveData["title"],
        "%s-%s-%s" % (
            liveData["area_name"], 
            liveData["area_v2_parent_name"], 
            liveData["area_v2_name"]
        ),
        image(liveData["cover_from_user"]),
        # "[CQ:image,file=https://i0.hdslb.com/bfs/live/d00325be2c9fcb62de54204c183db070daa6dbf4.png]",
        "https://live.bilibili.com/%s" % liveData["room_id"],
    )

def print_log(msg):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dir_path = os.path.dirname(os.path.abspath(__file__)) + '/logs'
    print(f'{__method__} + log_dir_path: {dir_path}')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    with open(f'{dir_path}/whzy_notice_{now[0:10]}.log', 'a') as f:
        f.write("Time: " + now + msg)

def write_live_status(status, file_path):
    # dir_path = '/home/ln/live_status'
    # if not os.path.exists(dir_path):
    #     os.mkdir(dir_path)

    with open(file_path, 'w') as f:
        f.write(str(status))

# 查看开播状态是否改变
def check_live_status(status, file_path):
    file_obj = open(file_path, "r")
    try:
        is_change = not str(status) in file_obj.read()
        file_obj.close()
        if is_change:
            return True
        else:
            return False
    except Exception as e:
        print_log("\nException: " + str(e) +
                  "\nLine: " + str(e.__traceback__.tb_lineno))

#测试 python /home/ln/whzy_live_notice.py dev
if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) > 1 else None
    is_dev = env == "dev"
    if is_dev:
        print("environment：" + sys.argv[1])
    uids = ['273083369'] if is_dev else ['355071645']
    # 改为群组
    group_ids = [232691961, 318103060] if is_dev else [709743734, 425278381, 833029738, 643249750]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = f'{script_dir}/dev_live_status/whzy_pick_foot' if is_dev else f'{script_dir}/live_status/whzy_eat_shit'
    response = get_bili_live_msg(uids)
    try:
        if response.status_code == 200:
            live_data = json.loads(response.text)["data"][uids[0]]
            live_status = live_data["live_status"] == 1
            print(f"检测开播状态是否改变：{check_live_status(live_status, file_path)}")
            print(f"实际开播状态：{live_status}")
            print(f"群通知，群号：{group_ids}")
            if check_live_status(live_status, file_path):
                if live_status:
                    msg = set_live_message(live_data)
                    # 艾特全体
                    if not is_dev:
                        # print(f"群艾特，群号：{group_ids}")
                        send_to_qq('[CQ:at,qq=all]', group_ids)
                else:
                    msg = set_live_end_message(live_data)
                write_live_status(live_status, file_path)
                
                # print(f"群通知，群号：{group_ids}")
                send_to_qq(msg, group_ids)
        else:
            print_log("\n[status_code]: " + str(response.status_code) +
                      "\n[text]:" + str(response.text))
                
    except Exception as e:
        print_log("\nException: " + str(e) +
                  "\nLine: " + str(e.__traceback__.tb_lineno))
