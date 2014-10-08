import robot

def program():
    r = robot.Robot()
    r.close_mouth()

    r.turn(90)
    r.drive_until_distance(16)
    r.turn(-90)
    r.drive(940)
    # we're near pos C
    if r.look_around(30, 50):
        if not r.eat_ball():
            print(":(")
            exit(1)
        r.turn(-90)
        r.drive(600)
        r.turn(-90)
        r.drive(950)
        r.avoid_wall(45, 50, 110, 30)
        r.drive(500)
        return
    # Not found in position C
    r.turn(-90)
    r.drive(600)
    r.turn(90)
    # we're near pos B
    if r.look_around(30, 50):
        if not r.eat_ball():
            print(":(")
            exit(1)
        r.turn(-180)
        r.drive(950)
        r.avoid_wall(45, 50, 110, 30)
        r.drive(500)
        return
    # Not found in position B
    r.turn(-90)
    r.drive(600)
    r.turn(90)
    # we're near pos A
    if r.look_around(30, 50):
        if not r.eat_ball():
            print(":(")
            exit(1)
        r.turn(90)
        r.drive(600)
        r.turn(90)
        r.drive(950)
        r.avoid_wall(45, 50, 110, 30)
        r.drive(500)
        return
    print("no ball!")

if __name__ == '__main__':
    program()
