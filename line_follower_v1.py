#!/usr/bin/env python3

"""
This line follower can be used to collect test data
To classify digits or shapes, you can use the classifier counterpart that classifies based on a trained imported model
"""

# Import the EV3 library
from ev3dev.auto import *
from time import sleep

# Connect motors
left_motor = LargeMotor(OUTPUT_B)
assert left_motor.connected
right_motor = LargeMotor(OUTPUT_C)
assert right_motor.connected

# Connect touch sensor and three color sensors
ts = TouchSensor()
assert ts.connected
col_left = ColorSensor('in1')
assert col_left.connected
col_mid = ColorSensor('in2')
assert col_mid.connected
col_right = ColorSensor('in4')
assert col_right.connected

# Change color sensor mode
col_left.mode = 'COL-REFLECT'
col_mid.mode = 'COL-REFLECT'
col_right.mode = 'COL-REFLECT'


def run():
    sharp_left = False
    sharp_right = False
    while not ts.value():
        # case: straight line, correct path
        if col_left.value() > 40 and col_mid.value() < 10 and col_right.value() > 40:
            right_motor.run_forever(speed_sp=80)
            left_motor.run_forever(speed_sp=80)
        # case: sharp left-hand turn ahead, assure that robot doesn't hang up while turning with boolean
        elif col_left.value() < 10 and col_mid.value() < 10 and col_right.value() > 40:
            right_motor.run_forever(speed_sp=100)
            left_motor.run_forever(speed_sp=-100)
            sharp_left = True
        # case: sharp right-hand turn ahead, assure that robot doesn't hang up while turning with boolean
        elif col_left.value() > 40 and col_mid.value() < 10 and col_right.value() < 10:
            right_motor.run_forever(speed_sp=-100)
            left_motor.run_forever(speed_sp=100)
            sharp_right = True
        # case: robot is a little off, ensure right path through slight correction to the right
        elif col_left.value() < 40 and col_mid.value() < 10 and col_right.value() > 40:
            right_motor.run_forever(speed_sp=80)
            left_motor.run_forever(speed_sp=10)
        # case: robot is a little off, ensure right path through slight correction to the left
        elif col_left.value() > 40 and col_mid.value() < 10 and col_right.value() < 40:
            right_motor.run_forever(speed_sp=10)
            left_motor.run_forever(speed_sp=80)
        # case: left-hand turn ahead
        elif col_left.value() > 40 and col_mid.value() > 10 and col_right.value() < 40:
            right_motor.run_forever(speed_sp=-100)
            left_motor.run_forever(speed_sp=100)
        # case: right-hand turn ahead
        elif col_left.value() < 40 and col_mid.value() > 10 and col_right.value() > 40:
            right_motor.run_forever(speed_sp=100)
            left_motor.run_forever(speed_sp=-100)
        # cases: assure that sharp turn is correctly driven
        elif col_left.value() < 10 and col_mid.value() < 10 and col_right.value() < 10 and sharp_left:
            right_motor.run_forever(speed_sp=100)
            left_motor.run_forever(speed_sp=-100)
            sharp_left = False
        elif col_left.value() < 10 and col_mid.value() < 10 and col_right.value() < 10 and sharp_right:
            right_motor.run_forever(speed_sp=-100)
            left_motor.run_forever(speed_sp=100)
            sharp_right = False

        # Write sensor data to text file
        f.write(str(col_left.value()) + "," + str(col_mid.value()) + "," + str(col_right.value()) + "," + str(
            left_motor.speed) + "," + str(right_motor.speed) + "\n")

        sleep(0.1)


f = open("data.txt", "w+")
run()
left_motor.stop()
right_motor.stop()
f.close()
