import robot

def program():
    r = robot.Robot()
    print("Distance front: " + str(r.distance_front()))
    print("Ball captured?: " + str(r.ball_captured()))
    r.turn(-90)
    r.drive(1230)
    r.turn(90)
    r.drive(1180)

if __name__ == '__main__':
    program()
