import robot

def program:
    r = Robot()
    print("Distance front: " + r.distance_front())
    print("Ball captured?: " + r.ball_captured())

if __name__ == 'main':
    program()