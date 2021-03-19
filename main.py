"""Main"""
import sys
sys.stderr = open("error.log", "w")

import time
# import msvcrt
import os
import subprocess
import cv2
import sqlite3
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
    max_height = 80    # [cm]
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

    arg = input("コードを入力してください:")

    drone = Tello()
    drone.streamon()
    
    controller = TelloControl()
    controller.append(CoCo(lambda : drone.set_speed(10)))

    # DB取得(出庫時想定)
    if len(arg) > 0:

        fixed_mode = False

        dbname = './TelloRecords/records/db.sqlite3'
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        try:
            sql = "select pos_x, pos_y, pos_z from qrcodes_qr"
            sql += " where qr_code = '{}'".format(arg)
            cur.execute(sql)
        except Exception as ex:
            print('SQL ERROR: {}'.format(ex))
        finally:
            target_pos = cur.fetchall()
            print(target_pos)
            if len(target_pos[0]) == 3:

                controller.append(CoCo(drone.takeoff))

                target_x: int = target_pos[0][0]
                target_y: int = target_pos[0][1]
                target_z: int = target_pos[0][2]
                
                move_flg: bool = np.abs(target_x) >= 20
                pls_flg: bool = target_x > 0
                if move_flg & pls_flg:
                    controller.append(CoCo(lambda : drone.right(target_x), np.array([target_x, 0, 0])))
                if move_flg & pls_flg == False:
                    controller.append(CoCo(lambda : drone.left(-target_x), np.array([target_x, 0, 0])))
                move_flg = np.abs(target_y) >= 20
                pls_flg = target_y > 0
                if move_flg & pls_flg:
                    controller.append(CoCo(lambda : drone.up(target_y), np.array([0, target_y, 0])))
                if move_flg & pls_flg == False:
                    controller.append(CoCo(lambda : drone.down(-target_y), np.array([0, target_y, 0])))
                move_flg = np.abs(target_z) >= 20
                pls_flg = target_z > 0
                if move_flg & pls_flg:
                    controller.append(CoCo(lambda : drone.forward(target_z), np.array([0, 0, target_z])))
                if move_flg & pls_flg == False:
                    controller.append(CoCo(lambda : drone.back(-target_z), np.array([0, 0, target_z])))
                
                move_flg = np.abs(target_z) >= 20
                pls_flg = target_z > 0
                if move_flg & pls_flg:
                    controller.append(CoCo(lambda : drone.back(target_z), np.array([0, 0, -target_z])))
                if move_flg & pls_flg == False:
                    controller.append(CoCo(lambda : drone.forward(-target_z), np.array([0, 0, -target_z])))
                move_flg = np.abs(target_y) >= 20
                pls_flg = target_y > 0
                if move_flg & pls_flg:
                    controller.append(CoCo(lambda : drone.down(target_y), np.array([0, -target_y, 0])))
                if move_flg & pls_flg == False:
                    controller.append(CoCo(lambda : drone.up(-target_y), np.array([0, -target_y, 0])))
                move_flg: bool = np.abs(target_x) >= 20
                pls_flg: bool = target_x > 0
                if move_flg & pls_flg:
                    controller.append(CoCo(lambda : drone.left(target_x), np.array([-target_x, 0, 0])))
                if move_flg & pls_flg == False:
                    controller.append(CoCo(lambda : drone.right(-target_x), np.array([-target_x, 0, 0])))

                controller.append(CoCo(drone.land))

            cur.close()
            conn.close()

    if fixed_mode:
        # controller.append(CoCo(drone.takeoff))
        # #平行移動
        # controller.append(CoCo(lambda : drone.up(max_height), np.array([0, max_height, 0])))
        # for i in range(height_step):
        #     if i % 2 == 0:
        #         # drone.left(max_LR)
        #         controller.append(CoCo(lambda : drone.left(max_LR), np.array([-max_LR, 0, 0])))
        #     else:
        #         controller.append(CoCo(lambda : drone.right(max_LR), np.array([max_LR, 0, 0])))
        #     controller.append(CoCo(lambda : drone.down(max_height/height_step), np.array([0, (int)(-max_height/height_step), 0])))
        # controller.append(CoCo(drone.land))

        with open("commands.txt") as f:
            for line in f:
                if line.startswith("takeoff"):
                    controller.append(CoCo(drone.takeoff))
                if line.startswith("land"):
                    controller.append(CoCo(drone.land))
                if line.startswith("up"):
                    distance = int(line.replace("up ", ""))
                    controller.append(CoCo(lambda: drone.up(distance), np.array([0,distance,0])))
                if line.startswith("down"):
                    distance1 = int(line.replace("down ", ""))
                    controller.append(CoCo(lambda: drone.down(distance1), np.array([0,-distance1,0])))
                if line.startswith("left"):
                    distance2 = int(line.replace("left ", ""))
                    controller.append(CoCo(lambda: drone.left(distance2), np.array([-distance2,0,0])))
                if line.startswith("right"):
                    distance3 = int(line.replace("right ", ""))
                    controller.append(CoCo(lambda: drone.right(distance3), np.array([distance3,0,0])))
                if line.startswith("forward"):
                    distance4 = int(line.replace("forward ", ""))
                    controller.append(CoCo(lambda: drone.forward(distance4), np.array([0,0,distance4])))
                if line.startswith("back"):
                    distance5 = int(line.replace("back ", ""))
                    controller.append(CoCo(lambda: drone.back(distance5), np.array([0,0,-distance5])))

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
            
            # # キー入力
            # if msvcrt.kbhit():
            #     kb = msvcrt.getch()
            #     key = kb.decode()
            #     if key == 't':      # 離陸
            #         drone.takeoff()
            #     elif key == 'l':    # 着陸
            #         drone.land()
            #     elif key == 'w':    # 前進
            #         drone.forward(50)
            #     elif key == 's':    # 後進
            #         drone.back(50)
            #     elif key == 'a':    # 左移動
            #         drone.left(50)
            #     elif key == 'd':    # 右移動
            #         drone.right(50)
            #     elif key == 'q':    # 左旋回
            #         drone.ccw(50)
            #     elif key == 'e':    # 右旋回
            #         drone.cw(50)
            #     elif key == 'r':    # 上昇
            #         drone.up(50)
            #     elif key == 'f':    # 下降
            #         drone.down(50)
            #     elif key == 'p':    # 任意のタイミングでストップ
            #         #drone.send_command('stop')
            #         drone.send_command('emergency')
            
            # ウエイト(とりあえず固定で)
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

    drone.streamoff()


if __name__ == "__main__":
    main()
