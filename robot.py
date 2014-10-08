from ev3.lego import InfraredSensor
from ev3.lego import ColorSensor
from ev3.lego import LargeMotor
from ev3.ev3dev import Motor
import time

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

    def drive(self, distance_mm, block_until_done=True):
        print('drive '+str(distance_mm) + 'mm')
        distance_rotations_ratio = 360/103.0
        rel_position = distance_mm * distance_rotations_ratio;
        power = 600
        ramp = 1000
        self._rotate_track_rel(self.left_track, rel_position, power, ramp)
        self._rotate_track_rel(self.right_track, rel_position, power, ramp)
        if (block_until_done):
            return self.move_until_finished()
        else:
            return True

    def turn(self, degrees, block_until_done=True):
        print('turn '+str(degrees))
        ratio = 555/90.0
        rel_position = ratio * degrees;
        power = 400
        ramp = 400
        self._rotate_track_rel(self.left_track, rel_position, power, ramp)
        self._rotate_track_rel(self.right_track, -rel_position, power, ramp)
        if (block_until_done):
            return self.move_until_finished()
        else:
            return True

    def motors_running(self):
        return self.left_track.run or self.right_track.run

    def stop(self):
        self.left_track.stop()
        self.right_track.stop()
        self.left_track.reset()
        self.right_track.reset()

    def move_until_finished(self):
        print('move until finished')
        while (self.motors_running()):
            if (self.distance_front() < 10):
                self.stop()
                print('action interrupted')
                return False  # Was interrupted
            else:
                print('motors still running ' + str(self.motors_running()))
                time.sleep(0.1)
        return True  # Finished as planned

    def _rotate_track_rel(self, track, rel_position, power, ramp):
      track.position_mode=Motor.POSITION_MODE.RELATIVE
      track.run_position_limited(position_sp=rel_position,
                                 speed_sp=power,
                                 stop_mode=Motor.STOP_MODE.BRAKE,
                                 ramp_up_sp=ramp,
                                 ramp_down_sp=ramp)
