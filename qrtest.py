"""QR Read Test"""
import time
import cv2
from pyzbar import pyzbar
from easytello.tello import Tello

def main():
    """test module"""
    drone = Tello()
    drone.command()
    drone.streamon()
    time.sleep(10)
    frame = drone.read()
    drone.streamoff()
    if frame is None or frame.size == 0:
        print("frame is None")
        return

    #デバッグ用
    cv2.imshow("QR1", frame)
    cv2.waitKey(5000)

    #QR解析
    decoded_objs = pyzbar.decode(frame)

    if decoded_objs != []:
        #解析したQRの1個目を表示
        str_dec_obj = decoded_objs[0][0].decode('utf-8', 'ignore')
        print(f'QR cord: {str_dec_obj}')

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
