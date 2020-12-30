import json
import requests
import numpy as np

# URL = "http://127.0.0.1/qrcodes/jsontest"
# sess = requests.session()

# print(sess.get(URL))

# if 'csrftoken' in sess.cookies:
#     # Django 1.6 and up
#     csrftoken = sess.cookies['csrftoken']
# else:
#     # older versions
#     csrftoken = sess.cookies['csrf']

# # ヘッダ
# headers = {'Content-type': 'application/json', "X-CSRFToken": csrftoken}

# # 送信データ
# prm = {"param1": "python"}

# # JSON変換
# params = json.dumps(prm)

# # POST送信
# res = sess.post(URL, data=params, headers=headers)

# # 戻り値を表示
# print(json.loads(res.text))

class HTTPRequest:
    def __init__(self, url):
        self.sended = []
        self.URL = url
        self.sess = requests.session()

        print(self.sess.get(self.URL))

        if 'csrftoken' in self.sess.cookies:
            # Django 1.6 and up
            self.csrftoken = self.sess.cookies['csrftoken']
        else:
            # older versions
            self.csrftoken = self.sess.cookies['csrf']

        # ヘッダ
        self.headers = {'Content-type': 'application/json', "X-CSRFToken": self.csrftoken}

    def send_qr(self, qrcode, pos: np.ndarray):
        if self.sended.count(qrcode) > 0:
            return
        
        # 送信データ
        prm = {"qrcode": qrcode, "pos_x": pos.x, "pos_y": pos.y, "pos_z": pos.z}

        # JSON変換
        params = json.dumps(prm)

        # POST送信
        res = self.sess.post(self.URL, data=params, headers=self.headers)

        self.sended.append(qrcode)
        # 戻り値を表示
        #print(json.loads(res.text))
