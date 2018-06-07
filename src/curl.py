import requests

import time

# url = "http://localhost:8080/test/idx"

url = "http://msg.umeng.com/api/send?sign=mysign"

params = {"policy":{"expire_time":"2018-05-03 17:39:24"},"description":"test_123","production_mode":"true","appkey":"5ae181688f4a9d6e360001d8","payload":{"body":{"title":"嘿嘿嘿嘿","ticker":"嘿嘿嘿嘿","text":"test81771","after_open":"go_app","play_vibrate":"false","play_lights":"false","play_sound":"true"},"display_type":"notification"},"type":"broadcast","timestamp":"1525254240754"}

h = {"content-type":"application/json"}

ret = requests.post(url,headers=h, data = params)

print(params)

print(ret.text)

# print(ret.headers)