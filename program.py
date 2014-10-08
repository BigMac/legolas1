import robot

def program():
    r = robot.Robot()
    print("Distance front: " + str(r.distance_front()))
    print("Ball captured?: " + str(r.ball_captured()))
    r.close_mouth()
    r.avoid_wall(45, 50, 110, 30)
#    r.open_mouth()
    r.drive(500, power=2000)
    return

#    r.avoid_wall(30, 50, 100, 30)
#    r.drive_until_distance(10)
#    r.turn(90)
#    r.drive_until_distance(16)
#    r.turn(-90)
#    r.drive(1080)
    if r.look_around(30, 40):
        r.eat_ball()

if __name__ == '__main__':
    program()
