from ev3.lego import InfraredSensor
from ev3.lego import ColorSensor

class Robot:
    def __init__(self):
        self.ir = InfraredSensor()
        self.color = ColorSensor()
    
    def distance_front(self):
        return self.ir.prox
    
    def ball_captured(self):
        while True:
            try:
                return self.color.reflect > 0
            except IOError:
                pass # this sometimes happens, try again
    