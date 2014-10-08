from ev3.lego import InfraredSensor
from ev3.lego import ColorSensor
from ev3.lego import LargeMotor
from ev3.ev3dev import Motor

class Robot:
    def __init__(self):
        self.ir = InfraredSensor()
        self.color = ColorSensor()
        self.left_track = LargeMotor(Motor.PORT.D)
        self.right_track = LargeMotor(Motor.PORT.A)

    def distance_front(self):
        return self.ir.prox

    def ball_captured(self):
        while True:
            try:
                return self.color.reflect > 0
            except IOError:
                pass # this sometimes happens, try again

    def turn(self, degrees):
        pass

    def drive(self, distance_mm, power):
        distance_rotations_ratio = 360/103.0
        self.left_track.position_mode=Motor.POSITION_MODE.RELATIVE
        self.right_track.position_mode=Motor.POSITION_MODE.RELATIVE
        self.left_track.run_position_limited(position_sp=distance_mm * distance_rotations_ratio, speed_sp=600,
            stop_mode=Motor.STOP_MODE.BRAKE , ramp_up_sp=1000, ramp_down_sp=1000)
        self.right_track.run_position_limited(position_sp=distance_mm * distance_rotations_ratio, speed_sp=600,
            stop_mode=Motor.STOP_MODE.BRAKE , ramp_up_sp=1000, ramp_down_sp=1000)

    def turn(self, degrees, power):
        atio = 360/103.0
        self.left_track.position_mode=Motor.POSITION_MODE.RELATIVE
        self.right_track.position_mode=Motor.POSITION_MODE.RELATIVE
        self.left_track.run_position_limited(position_sp=555, speed_sp=400,
            stop_mode=Motor.STOP_MODE.BRAKE , ramp_up_sp=400, ramp_down_sp=400)
        self.right_track.run_position_limited(position_sp=-555, speed_sp=400,
            stop_mode=Motor.STOP_MODE.BRAKE , ramp_up_sp=400, ramp_down_sp=400)
