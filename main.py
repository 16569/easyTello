"""Main"""
import time
import msvcrt
import os
import subprocess
import cv2
import numpy as np
from pyzbar import pyzbar
from easytello.tello import Tello
from httprequest import HTTPRequest
from easytello.tello_control import ControlCommand as CoCo
from easytello.tello_control import TelloControl

def main():
    """
    ストリーミングでQRを解析しながら
    DjangoサーバーにHTTPリクエストする
    """
    #|パラメータ
    #|--固定ルートモード
    fixed_mode = True
    max_height = 50    # [cm]
    max_LR = 100        # [cm]
    height_step = 1     # 段差数
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

    drone = Tello()
    drone.streamon()
    
    controller = TelloControl()
    controller.append(CoCo(lambda : drone.set_speed(10)))

    if fixed_mode:
        controller.append(CoCo(drone.takeoff))
        #平行移動
        controller.append(CoCo(lambda : drone.up(max_height), np.array([0, max_height, 0])))
        for i in range(height_step):
            if i % 2 == 0:
                drone.left(max_LR)
                controller.append(CoCo(lambda : drone.left(max_LR), np.array([-max_LR, 0, 0])))
            else:
                controller.append(CoCo(lambda : drone.right(max_LR), np.array([max_LR, 0, 0])))
            controller.append(CoCo(lambda : drone.down(max_height/height_step), np.array([0, (int)(-max_height/height_step), 0])))
        controller.append(CoCo(drone.land))

    drone.set_controller(controller)

    #ストリーミングをONにしたらN秒間待機
    time.sleep(5)

    controller.start()

    req = None
    if request_enable:
        req = HTTPRequest(request_url)
    
    try:
        while True:
            frame = drone.read()
            #cv2.imshow('DJI Tello', frame)
            # QR解析
            if frame is not None:
                decoded_objs = pyzbar.decode(frame)
                if decoded_objs != []:
                    # 解析した1個目を表示
                    str_dec_obj = decoded_objs[0][0].decode('utf-8', 'ignore')
                    print(f'QR cord: {str_dec_obj}')
                    # 解析時の座標
                    pos = drone.get_position()
                    # HTTP送信
                    if request_enable:
                        req.send_qr(str_dec_obj, pos)
            
            # キー入力
            if msvcrt.kbhit():
                kb = msvcrt.getch()
                key = kb.decode()
                if key == 't':      # 離陸
                    drone.takeoff()
                elif key == 'l':    # 着陸
                    drone.land()
                elif key == 'w':    # 前進
                    drone.forward(50)
                elif key == 's':    # 後進
                    drone.back(50)
                elif key == 'a':    # 左移動
                    drone.left(50)
                elif key == 'd':    # 右移動
                    drone.right(50)
                elif key == 'q':    # 左旋回
                    drone.ccw(50)
                elif key == 'e':    # 右旋回
                    drone.cw(50)
                elif key == 'r':    # 上昇
                    drone.up(50)
                elif key == 'f':    # 下降
                    drone.down(50)
                elif key == 'p':    # 任意のタイミングでストップ
                    #drone.send_command('stop')
                    drone.send_command('emergency')
            
            # ウエイト(とりあえず固定で)
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

    drone.streamoff()


if __name__ == "__main__":
    main()
