import robot
import program
import time
import wall
import os
import subprocess
from ev3.ev3dev import Key

def start():
    r = robot.Robot()
    k = Key()
    while True:
        time.sleep(0.1)
        if k.down:
            wall.program()
            time.sleep(1)
        if k.up:
            program.program()
            time.sleep(1)
        if k.backspace:
            time.sleep(1)
            if k.backspace:
                os.system("shutdown -h 0")
        if k.left:
            subprocess.call(["aplay", "badumtss.wav"])
        if k.right:
            subprocess.call(["aplay", "drama.wav"])


if __name__ == '__main__':
    start()
