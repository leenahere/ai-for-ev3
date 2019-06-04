#!/usr/bin/env python3

"""
This line follower can be used to collect test data
To classify digits or shapes, you can use the classifier counterpart that classifies based on a trained imported model
This is the better line following algorithm, but:
The trained models and the train and test data in the data folder were collected with the v1 line follower
Therefore, when working with this line follower, it's best to collect your own data with this script
"""

# Import the EV3-robot library
from ev3dev.auto import *

# Connect motors
left_motor = LargeMotor(OUTPUT_B)
assert left_motor.connected
right_motor = LargeMotor(OUTPUT_C)
assert right_motor.connected

# Connect touch sensor and color sensors
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
    left = []
    middle = []
    right = []

    while not ts.value():
        # Add sensor values to respective list
        left.append(col_left.value())
        middle.append(col_mid.value())
        right.append(col_right.value())

        # As long as the color sensor in the middle is on the black line, the robot should drive straight
        if middle[-1] < 10:
            right_motor.run_forever(speed_sp=90)
            left_motor.run_forever(speed_sp=90)

        # Once all three sensors only see white surface, iterate through the right and left sensor list
        if left[-1] > 40 and middle[-1] > 40 and right[-1] > 40:
            found = False
            iterator = -2
            while not found:
                # Depending on the sensor that last saw the black line, turn right or left
                if left[iterator] < 10:
                    right_motor.run_forever(speed_sp=100)
                    left_motor.run_forever(speed_sp=-100)
                    found = True
                if right[iterator] < 10:
                    right_motor.run_forever(speed_sp=-100)
                    left_motor.run_forever(speed_sp=100)
                    found = True
                iterator -= 1
                # Make sure that list index isn't out of range
                if abs(iterator) > len(left) or abs(iterator) > len(right):
                    break

        # Write sensor data to text file
        f.write(str(col_left.value()) + "," + str(col_mid.value()) + "," + str(col_right.value()) + "," + str(
            left_motor.speed) + "," + str(right_motor.speed) + "\n")


f = open("data.txt", "w+")
run()
left_motor.stop()
right_motor.stop()
f.close()
