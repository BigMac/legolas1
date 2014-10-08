import robot
import program
import time
import wall
import os
from ev3.ev3dev import Key

def program():
    r = robot.Robot()
    k = Key()
    while True:
        time.sleep(0.1)
        if k.up:
            wall.program()
            time.sleep(1)
        if k.backspace:
            os.system("shutdown -h 0")   
	

if __name__ == '__main__':
    program()
