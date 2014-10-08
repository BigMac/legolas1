import robot

def program():
    r = robot.Robot()
    r.close_mouth()

    approach_distance = 940
    return_distance = 900
    distance_between_targets = 600
    right = 90
    left = -90
    around = 180

    r.turn(right)
    r.drive_until_distance(16)
    r.turn(left)
    r.drive(approach_distance)
    # we're near pos C
    if r.look_around(30, 50):
        print("Found ball at position C")
        if not r.eat_ball():
            print(":(")
            exit(1)
        r.turn(left)
        r.drive(distance_between_targets)
        r.turn(left)
        r.drive(return_distance)
        r.avoid_wall(45, 50, 110, 30)
        r.drive(500)
        return
    # Not found in position C
    r.turn(left)
    r.drive(distance_between_targets)
    r.turn(right)
    # we're near pos B
    if r.look_around(30, 50):
        print("Found ball at position B")
        if not r.eat_ball():
            print(":(")
            exit(1)
        r.turn(around)
        r.drive(return_distance)
        r.avoid_wall(45, 50, 110, 30)
        r.drive(500)
        return
    # Not found in position B
    r.turn(left)
    r.drive(distance_between_targets)
    r.turn(right)
    # we're near pos A
    if r.look_around(30, 50):
        print("Found ball at position A")
        if not r.eat_ball():
            print(":(")
            exit(1)
        r.turn(right)
        r.drive(distance_between_targets)
        r.turn(right)
        r.drive(return_distance)
        r.avoid_wall(45, 50, 110, 30)
        r.drive(500)
        return
    print("no ball!")

if __name__ == '__main__':
    program()
