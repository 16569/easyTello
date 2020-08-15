"""Main"""
import time
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

    # #サーバー起動
    # command = [
    #     "python", 
    #     "./TelloRecords/records/manage.py", 
    #     "runserver", 
    #     "0.0.0.0:80"
    #     ]
    # subprocess.Popen(command)
    # time.sleep(10)
    # os.system("start http://127.0.0.1/qrcodes/")
   
    #パラメータ
    max_height = 100    #(cm)
    max_LR = 100        #(cm)
    height_step = 4     #段差数

    drone = Tello()
    drone.command()
    drone.streamon()

    #ストリーミングをONにしたらN秒間待機
    time.sleep(5)
    
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

    req = HTTPRequest()
    try:
        while True:
            frame = drone.read()
            #QR解析
            decoded_objs = pyzbar.decode(frame)
            if decoded_objs != []:
                #解析したQRの1個目を表示
                str_dec_obj = decoded_objs[0][0].decode('utf-8', 'ignore')
                print(f'QR cord: {str_dec_obj}')
                req.send(str_dec_obj)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    drone.streamoff()


if __name__ == "__main__":
    main()
