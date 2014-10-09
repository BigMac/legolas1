import robot
import program
import time
import program
import os
from ev3.ev3dev import Key

def start():
    r = robot.Robot()
    k = Key()
    while True:
        time.sleep(0.1)
        if k.up:
            program.program()
            time.sleep(1)
        if k.backspace:
            os.system("shutdown -h 0")   
	

if __name__ == '__main__':
    start()
