import robot

def program():
    r = robot.Robot()
    print("Distance front: " + str(r.distance_front()))
    print("Ball captured?: " + str(r.ball_captured()))
    r.drive(240, 20)

if __name__ == '__main__':
    program()
