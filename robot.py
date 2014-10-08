from ev3.lego import InfraredSensor
from ev3.lego import ColorSensor
from ev3.lego import LargeMotor
from ev3.lego import MediumMotor
from ev3.ev3dev import Motor
import time

class Robot:
    def __init__(self):
        self.ir = InfraredSensor()
        self.color = ColorSensor()
        self.left_track = LargeMotor(Motor.PORT.D)
        self.right_track = LargeMotor(Motor.PORT.A)
        self.mouth = MediumMotor(Motor.PORT.B)

    def distance_front(self):
        return self.ir.prox

    def ball_captured(self):
        while True:
            try:
                return self.color.reflect > 0
            except IOError:
                pass # this sometimes happens, try again

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

    def drive_until_distance(self, ir_distance):
        print('driving until ir shows ' + str(ir_distance))
        self.drive(20000, False)
        while (self.distance_front() > ir_distance):
            time.sleep(0.1)
        self.stop()

    def turn(self, degrees, block_until_done=True):
        print('turn '+str(degrees))
        ratio = 555/90.0
        rel_position = ratio * degrees;
        power = 400
        ramp = 400
        self._rotate_track_rel(self.left_track, -rel_position, power, ramp)
        self._rotate_track_rel(self.right_track, rel_position, power, ramp)
        if (block_until_done):
            return self.move_until_finished()
        else:
            return True

    def motors_running(self):
        return self.left_track.state != 'idle' or self.right_track.state != 'idle'

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
                print('distance ' + str(self.distance_front()))
                time.sleep(0.1)
        return True  # Finished as planned

    def open_mouth(self):
        self._move_mouth(-5*360)

    def close_mouth(self):
        self._move_mouth(0)

    def _rotate_track_rel(self, track, rel_position, power, ramp):
      track.position_mode=Motor.POSITION_MODE.RELATIVE
      track.run_position_limited(position_sp=rel_position,
                                 speed_sp=power,
                                 stop_mode=Motor.STOP_MODE.BRAKE,
                                 ramp_up_sp=ramp,
                                 ramp_down_sp=ramp)

    def _move_mouth(self, position):
        self.mouth.position_mode=Motor.POSITION_MODE.ABSOLUTE
        self.mouth.run_position_limited(position_sp=position,
                                        speed_sp=1000,
                                        stop_mode=Motor.STOP_MODE.BRAKE)
