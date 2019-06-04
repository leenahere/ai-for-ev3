#!/usr/bin/env python3

"""
This line follower can be used to classify digits
To collect train and test data, use the counterpart line follower
This line follower often fails some digits due to their sharp angles
However, this classifier works really well with the trained models and the collected data
!! models and data haven't been trained on number 2 !!
"""

# Import the EV3 library
from ev3dev.auto import *
from time import sleep
import pickle

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
    sharp_left = False
    sharp_right = False

    left_sensor = 0
    mid_sensor = 0
    right_sensor = 0
    left_motor_count = 0
    right_motor_count = 0

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

        left_sensor += col_left.value()
        mid_sensor += col_mid.value()
        right_sensor += col_right.value()
        left_motor_count += left_motor.speed
        right_motor_count += right_motor.speed

        sleep(0.1)

    left_motor.stop()
    right_motor.stop()

    # Assure that values are comparable to train and test data by dividing the input by the longest data set from the
    # train and test data
    # This is kind of hacky and the 533 is specific to the data in the data folder
    # You need to alter this when you work with your own data
    left_sensor = left_sensor / 533
    mid_sensor = mid_sensor / 533
    right_sensor = right_sensor / 533
    left_motor_count = left_motor_count / 533
    right_motor_count = right_motor_count / 533

    X_new = [[left_sensor, mid_sensor, right_sensor, left_motor_count, right_motor_count]]

    # Load model
    loaded_model = pickle.load(open('./digit_models/trained_model.sav', 'rb'))
    loaded_scaler = pickle.load(open('./digit_models/mlp_scaler.pkl', 'rb'))

    # Apply scaler
    X_new = loaded_scaler.transform(X_new)

    # Classify new data
    y_new = loaded_model.predict(X_new)
    print(str(y_new[0]))
    Sound.speak(str(y_new[0]))


run()
