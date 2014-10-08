import robot
import time
from ev3.ev3dev import Key

def program():
    r = robot.Robot()
    while True:
        r.keys()
        time.sleep(500)

if __name__ == '__main__':
    program()
