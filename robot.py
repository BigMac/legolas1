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

    def drive(self, distance_mm):
        distance_rotations_ratio = 360/103.0
        rel_position = distance_mm * distance_rotations_ratio;
        power = 600
        ramp = 1000
        _rotate_track_rel(self.left_track, rel_position, power, ramp)
        _rotate_track_rel(self.right_track, rel_position, power, ramp)

    def turn(self, degrees):
        ratio = 555/90.0
        rel_position = ratio * degrees;
        power = 400
        ramp = 400
        _rotate_track_rel(self.left_track, rel_position, power, ramp)
        _rotate_track_rel(self.right_track, -rel_position, power, ramp)

    def _rotate_track_rel(self, track, rel_position, power, ramp):
      track.position_mode=Motor.POSITION_MODE.RELATIVE)
      track.run_position_limited(position_sp=rel_position,
                                 speed_sp=power,
                                 stop_mode=Motor.STOP_MODE.BRAKE,
                                 ramp_up_sp=ramp,
                                 ramp_down_sp=ramp)
