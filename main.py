"""Main"""
import time
import msvcrt
import os
import subprocess
from pyzbar import pyzbar
from easytello.tello import Tello
from httprequest import HTTPRequest

def main():
    """
    ストリーミングでQRを解析しながら
    DjangoサーバーにHTTPリクエストする
    """
    #|パラメータ
    #|--固定ルートモード
    fixed_mode = True
    max_height = 100    # [cm]
    max_LR = 100        # [cm]
    height_step = 4     # 段差数
    #|--HTTPリクエスト
    request_enable = True
    request_url = "http://127.0.0.1/qrcodes/jsontest"

    # #サーバー起動
    # command = [
    #     "python", 
    #     "./TelloRecords/records/manage.py", 
    #     "runserver", 
    #     "0.0.0.0:80"
    #     ]
    # subprocess.Popen(command)
    # time.sleep(10)
    # #ブラウザ起動
    # os.system("start http://127.0.0.1/qrcodes/")

    # ここからTelloの操作開始
    drone = Tello()
    drone.command()
    drone.streamon()
    drone.set_speed(10)

    #ストリーミングをONにしたらN秒間待機
    time.sleep(5)
    
    if fixed_mode:
        drone.takeoff()
        #平行移動
        drone.up(max_height)
        for i in range(height_step):
            if i % 2 == 0:
                drone.right(max_LR)
            else:
                drone.left(max_LR)
            drone.down(max_height/height_step)
        drone.land()

    req = None
    if request_enable:
        req = HTTPRequest(request_url)
    
    try:
        while True:
            frame = drone.read()
            # QR解析
            decoded_objs = pyzbar.decode(frame)
            if decoded_objs != []:
                # 解析した1個目を表示
                str_dec_obj = decoded_objs[0][0].decode('utf-8', 'ignore')
                print(f'QR cord: {str_dec_obj}')
                # HTTP送信
                if request_enable:
                    req.send_qr(str_dec_obj)
            
            # キー入力
            if msvcrt.kbhit():
                kb = msvcrt.getch()
                key = kb.decode()
                if key == 't':      # 離陸
                    drone.takeoff()
                elif key == 'l':    # 着陸
                    drone.land()
                elif key == 'w':    # 前進
                    drone.forward(20)
                elif key == 's':    # 後進
                    drone.back(20)
                elif key == 'a':    # 左移動
                    drone.left(20)
                elif key == 'd':    # 右移動
                    drone.right(20)
                elif key == 'q':    # 左旋回
                    drone.ccw(20)
                elif key == 'e':    # 右旋回
                    drone.cw(20)
                elif key == 'r':    # 上昇
                    drone.up(20)
                elif key == 'f':    # 下降
                    drone.down(20)
                elif key == 'p':    # 任意のタイミングでストップ
                    drone.send_command('stop')
            
            # ウエイト(とりあえず固定で)
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass

    drone.streamoff()


if __name__ == "__main__":
    main()
