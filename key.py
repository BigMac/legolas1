import robot
import time
from ev3.ev3dev import Key

def program():
    r = robot.Robot()
    while True:
        k = Key()
        print(str(k.up))
        print(str(k.__dict__))
        time.sleep(500)

    while True:
        r.keys()

if __name__ == '__main__':
    program()