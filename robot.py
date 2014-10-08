from ev3.lego import InfraredSensor
from ev3.lego import ColorSensor
from ev3.lego import LargeMotor
from ev3.lego import MediumMotor
from ev3.ev3dev import Key
from ev3.ev3dev import LED
from ev3.ev3dev import Motor
import time

class Robot:
    def __init__(self):
        self.ir = InfraredSensor()
        self.color = ColorSensor()
        self.left_track = LargeMotor(Motor.PORT.D)
        self.right_track = LargeMotor(Motor.PORT.A)
        self.mouth = MediumMotor(Motor.PORT.B)
        self.key = Key()
        self.led = LED()
        self.reset_leds()

    def reset_leds(self):
        self.led.left.on()
        self.led.right.on()
        self.led.left.color = LED.COLOR.GREEN
        self.led.right.color = LED.COLOR.GREEN


    def keys(self):
        keys = ('up', 'down', 'left', 'right', 'backspace', 'enter')
        dump = [x + ":" + str(self.key.__dict__[x]) for x in keys]
        print " ".join(dump)
        return self.key

    def distance_front(self):
        return self.ir.prox

    def ball_captured(self):
        while True:
            try:
                return self.color.reflect > 0
            except IOError:
                pass # this sometimes happens, try again

    def drive(self, distance_mm, block_until_done=True, power=600):
        self.led.left.color = LED.COLOR.AMBER
        print('drive '+str(distance_mm) + 'mm')
        distance_rotations_ratio = 360/103.0
        rel_position = distance_mm * distance_rotations_ratio
        ramp = 1000
        self._rotate_track_rel(self.left_track, rel_position, power, ramp)
        self._rotate_track_rel(self.right_track, rel_position, power, ramp)
        if (block_until_done):
            return self.move_until_finished(distance_mm < 0)
        else:
            self.reset_leds()
            return True

    def drive_until_distance(self, ir_distance):
        self.led.right.color = LED.COLOR.AMBER
        print('driving until ir shows ' + str(ir_distance))
        self.drive(20000, False)
        while (self.distance_front() > ir_distance):
            time.sleep(0.1)
        self.stop()
        self.reset_leds()

    def turn(self, degrees, block_until_done=True):
        print('turn '+str(degrees))
        ratio = 545 / 90.0
        if degrees > 0:
            led = self.led.right
        else:
            led = self.led.left
        led.blink(color=LED.COLOR.AMBER, delay_on=100, delay_off=200)
        rel_position = ratio * degrees
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
        self.right_track.stop()
        self.left_track.stop()
        self.left_track.reset()
        self.right_track.reset()

    def move_until_finished(self, reverse=False):
        print('move until finished')
        while (self.motors_running()):
            if not reverse and self.distance_front() < 10:
                self.stop()
                print('action interrupted')
                return False  # Was interrupted
            else:
                print('distance ' + str(self.distance_front()))
                time.sleep(0.1)
        self.reset_leds()
        return True  # Finished as planned

    def avoid_wall(self, degrees_each, threshold=50, backoff_mm=100, backoff_angle=30):
        if self.distance_front() < 30:
            self.drive(-backoff_mm)
        self.turn(-degrees_each, True)
        self.turn(degrees_each, False)
        found_neg, max_neg = self.move_until_moving_away(threshold)
        self.turn(degrees_each, True)
        self.turn(-degrees_each, False)
        found_pos, max_pos = self.move_until_moving_away(threshold)

        #max_pos = max(80, max_pos)
        #max_neg = max(80, max_pos)

        correction = 0
        scale = 1
        print("positive degrees: " + str(found_pos) + ", " + str(max_pos))
        print("negative degrees: " + str(found_neg) + ", " + str(max_neg))
        if found_pos and not found_neg:
            correction = -1
        elif found_neg and not found_pos:
            correction = 1
        elif found_pos and found_neg:
            scale = 2
            if max_pos > max_neg:
                correction = 1
            elif max_neg > max_pos:
                correction = -1

        print("correction: " + str(correction) + ", scale: " + str(scale))
        if correction != 0:
            self.drive(-backoff_mm * scale)
            self.turn(backoff_angle * correction)
            self.drive(backoff_mm * scale)
            return True

        return False

    def move_until_moving_away(self, threshold, current_min=99):
        max_distance = 0
        found = False
        while self.motors_running() and self.distance_front() > threshold:
            max_distance = max(max_distance, self.distance_front())
            print('find object a ' + str(self.distance_front()) + " / " + str(max_distance))
            time.sleep(0.05)
        if self.distance_front() <= threshold:
            min_distance = current_min
            while self.motors_running():
                current_distance = self.distance_front()
                max_distance = max(max_distance, self.distance_front())
                print('find object b ' + str(self.distance_front()) + " / " + str(max_distance))
                print('find object b ' + str(min_distance) + " / " + str(max_distance))
                if current_distance <= min_distance:
                    min_distance = current_distance
                else:
                    found = True
            found = True
        while self.motors_running():
            print('find object c ' + str(self.distance_front()) + " / " + str(max_distance))
            max_distance = max(max_distance, self.distance_front())
            time.sleep(0.05)
        return found, max_distance



    def look_around(self, degrees_each, threshold=20):
        min_distance = self.distance_front()
        self.turn(-degrees_each, True)
        self.turn(degrees_each * 2, False)
        while self.motors_running() and self.distance_front() > threshold:
            time.sleep(0.05)

        if self.distance_front() <= threshold:
            min_distance = self.distance_front()
            while self.motors_running():
                current_distance = self.distance_front()
                if current_distance <= min_distance:
                    min_distance = current_distance
                else:
                    self.stop()
                    print('stopping at ' + str(current_distance))
                    return True # todo calculate the angle we ended up at

        self.move_until_finished()
        self.turn(-degrees_each, True)

    def open_mouth(self):
        self._move_mouth(-5*360)

    def close_mouth(self):
        self._move_mouth(0)

    def eat_ball(self):
        """Assumes ball is in front, close enough"""
        captured = False
        self.open_mouth()
        self.drive(300, False)
        while (self.motors_running()):
            if (self.ball_captured()):
                self.close_mouth()
                captured = True
            else:
                time.sleep(0.05)
        self.close_mouth()
        self.drive(-300, True)
        return captured

    def get_absolute_track_positions(self):
        return (self.left_track.position, self.right_track.position)

    def restore_absolute_track_positions(self, positions, power, ramp):
        print('Current track positions: ' + str(self.get_absolute_track_positions()))
        print('Want to restore: ' + str(positions))
        self._rotate_track_abs(self.left_track, positions[0], power, ramp)
        self._rotate_track_abs(self.right_track, positions[1], power, ramp)

    def _rotate_track_rel(self, track, rel_position, power, ramp):
        track.position_mode = Motor.POSITION_MODE.RELATIVE
        track.run_position_limited(position_sp=rel_position,
                                   speed_sp=power,
                                   stop_mode=Motor.STOP_MODE.BRAKE,
                                   ramp_up_sp=ramp,
                                   ramp_down_sp=ramp)

    def _rotate_track_abs(self, track, abs_position, power, ramp):
        track.position_mode = Motor.POSITION_MODE.ABSOLUTE
        track.run_position_limited(position_sp=abs_position,
                                   speed_sp=power,
                                   stop_mode=Motor.STOP_MODE.BRAKE,
                                   ramp_up_sp=ramp,
                                   ramp_down_sp=ramp)

    def _move_mouth(self, position):
        self.mouth.position_mode = Motor.POSITION_MODE.ABSOLUTE
        self.mouth.run_position_limited(position_sp=position,
                                        speed_sp=1000,
                                        stop_mode=Motor.STOP_MODE.BRAKE)
        while (self.mouth.state != 'idle'):
            time.sleep(0.1)
