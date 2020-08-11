"""Flight Plan"""
from easytello.tello import Tello

def main():
    """test module"""
    max_height = 100    #(cm)
    max_LR = 100        #(cm)
    height_step = 4     #段差数

    drone = Tello()
    drone.command()
    drone.takeoff()

    #平行移動
    drone.up(max_height)
    for i in range(height_step):
        if i % 2 == 0:
            drone.right(max_LR)
        else:
            drone.left(max_LR)
        drone.down(max_height / height_step)
    drone.land()

if __name__ == "__main__":
    main()
