import robot

def program():
    r = robot.Robot()
    r.close_mouth()

    approach_distance = 900
    return_distance = 800
    distance_between_targets = 600
    right = 90
    left = -90
    around = 180

    r.drive(100)
    r.turn(right)
    r.drive_until_distance(16)
    r.turn(left)
    r.drive(approach_distance)
    # we're near pos C
    if r.look_around(30, 55):
        print("Found ball at position C")
        r.eat_ball()
        r.turn(left)
        r.drive(distance_between_targets)
        r.turn(left)
        r.drive(return_distance)
        r.avoid_wall(45, 50, 110, 30)
        r.drive(800)
        r.music("badumtss")
        return
    # Not found in position C
    r.turn(left)
    r.drive(distance_between_targets)
    r.turn(right)
    r.drive(50)
    # we're near pos B
    if r.look_around(30, 55):
        print("Found ball at position B")
        r.eat_ball()
        r.turn(around)
        r.drive(return_distance)
        r.avoid_wall(45, 50, 110, 30)
        r.drive(800)
        r.music("badumtss")
        return
    # Not found in position B
    r.turn(left)
    r.drive(distance_between_targets)
    r.turn(right)
    r.drive(50)
    # we're near pos A
    if r.look_around(30, 55, True):
        print("Found ball at position A")
        r.eat_ball()
        r.turn(right)
        r.drive(distance_between_targets)
        r.turn(right)
        r.drive(return_distance)
        r.avoid_wall(45, 50, 110, 30)
        r.drive(800)
        r.music("badumtss")
        return
    print("no ball!")
    r.music("drama")

if __name__ == '__main__':
    program()
