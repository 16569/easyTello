import json
import requests

URL = "http://127.0.0.1/qrcodes/jsontest"
sess = requests.session()

print(sess.get(URL))

if 'csrftoken' in sess.cookies:
    # Django 1.6 and up
    csrftoken = sess.cookies['csrftoken']
else:
    # older versions
    csrftoken = sess.cookies['csrf']

# ヘッダ
headers = {'Content-type': 'application/json', "X-CSRFToken": csrftoken}

# 送信データ
prm = {"param1": "python"}

# JSON変換
params = json.dumps(prm)

# POST送信
res = sess.post(URL, data=params, headers=headers)

# 戻り値を表示
print(json.loads(res.text))
