import robot

def program():
    r = robot.Robot()
    r.close_mouth()

    r.turn(90)
    r.drive_until_distance(16)
    r.turn(-90)
    r.drive(940)
    if r.look_around(30, 50):
        if not r.eat_ball():
            print(":(")
            exit(1)
        r.turn(-90)
        r.drive(500)
        r.turn(-90)
        r.drive(950)
        r.avoid_wall(45, 50, 110, 30)
        r.drive(500)
        

if __name__ == '__main__':
    program()
