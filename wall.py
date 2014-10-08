import robot

def program():
    r = robot.Robot()
    r.close_mouth()
    r.avoid_wall(45, 50, 110, 30)
    r.open_mouth()
    r.drive(500, power=2000)
    r.close_mouth()

if __name__ == '__main__':
    program()
