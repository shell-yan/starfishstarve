import re
import json
import requests
import random
import time
from https://www.plurk.com/starfishhungry import PlurkAPI

# Plurk API 認證
plurk = PlurkAPI('DDoPEkyGXNd2', 'WOSxyGxr1vQbmip6hNdmBSrU78NgW8hO')
plurk.authorize('avJGJBqdfD3P', 'v34XamJ3097vMTgZEPYYJUm2f5x3lDUU')

# 食物清單
food_list = ["咖哩扮飯!", "珍珠粉條仙草凍", "紅酒燉牛肉", "酸辣粉", "烤肉", "披薩", "肉桂捲", "薯條", "芋頭火鍋", "烤肉", "車輪餅", "地瓜球"]
other_list = ["答辯", "那海星餓餓獸說想要吃ㄋㄋ", "闢眼"]

# 設置即時更新通道
try:
    comet = plurk.callAPI('/APP/Realtime/getUserChannel')
    comet_channel = comet.get('comet_server') + "&new_offset=%d"
    jsonp_re = re.compile('CometChannel.scriptCallback\((.+)\);\s*')
    new_offset = -1
except Exception as e:
    print(f"Error in setting up comet channel: {e}")

while True:
    try:
        plurk.callAPI('/APP/Alerts/addAllAsFriends')
        response = requests.get(comet_channel % new_offset, timeout=80)
        rawdata = response.text
        match = jsonp_re.match(rawdata)
        if match:
            rawdata = match.group(1)
        data = json.loads(rawdata)
        new_offset = data.get('new_offset', -1)
        msgs = data.get('data')
        if not msgs:
            continue
        for msg in msgs:
            if msg.get('type') == 'new_plurk':
                pid = msg.get('plurk_id')
                content = msg.get('content_raw')
                if "海星餓餓獸" in content or "吃什麼" in content:
                    food = random.choice(food_list)
                    plurk.callAPI('/APP/Responses/responseAdd', {
                        'plurk_id': pid,
                        'content': food,
                        'qualifier': ':'
                    })
            elif msg.get('type') == 'new_response':
                response_content = msg.get('response_content_raw')
                if "不要" in response_content or "換一個" in response_content:
                    food = random.choice(other_list)
                    plurk.callAPI('/APP/Responses/responseAdd', {
                        'plurk_id': pid,
                        'content': food,
                        'qualifier': ':'
                    })
                elif "屁眼" in response_content:
                    plurk.callAPI('/APP/Responses/responseAdd', {
                        'plurk_id': pid,
                        'content': "幹幹",
                        'qualifier': ':'
                    })
    except Exception as e:
        print(f"Error during execution: {e}")
    time.sleep(1)
