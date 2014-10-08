import robot
import time

def program():
    r = robot.Robot()
    while True:
        r.keys()
        time.sleep(500)

if __name__ == '__main__':
    program()
