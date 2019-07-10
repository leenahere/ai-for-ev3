#!/usr/bin/env python3

"""
This line follower can be used to classify digits
To collect train and test data, use the counterpart line follower
This is the better line following algorithm, but:
The trained models and the train and test data in the data folder were collected with the v1 line follower
Therefore, when working with this classifier, it's best to collect your own data with the counterpart line follower v2
"""

# Import the EV3-robot library
from ev3dev.auto import *
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

screen = Screen()


def run():
    left = []
    middle = []
    right = []

    left_sensor = 0
    mid_sensor = 0
    right_sensor = 0
    left_motor_count = 0
    right_motor_count = 0

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

        left_sensor += col_left.value()
        mid_sensor += col_mid.value()
        right_sensor += col_right.value()
        left_motor_count += left_motor.speed
        right_motor_count += right_motor.speed

    left_motor.stop()
    right_motor.stop()

    # Assure that values are comparable to train and test data by dividing the input by the longest data set from the
    # train and test data
    # This is kind of hacky and the 533 is specific to the data in the data folder
    # You need to alter this when you work with your own data
    left_sensor = left_sensor / 1883
    mid_sensor = mid_sensor / 1883
    right_sensor = right_sensor / 1883
    left_motor_count = left_motor_count / 1883
    right_motor_count = right_motor_count / 1883

    X_new = [[left_sensor, mid_sensor, right_sensor, left_motor_count, right_motor_count]]

    # Load model and scaler
    loaded_model = pickle.load(open('./binary_models/trained_model.sav', 'rb'))
    loaded_scaler = pickle.load(open('./binary_models/mlp_scaler.pkl', 'rb'))

    # Apply scaler
    X_new = loaded_scaler.transform(X_new)

    # Classify new data
    y_new = loaded_model.predict(X_new)

    if y_new[0] == 0:
        screen.clear()

        # Screen.draw returns a PIL.ImageDraw handle
        screen.draw.line((30, 50, 80, 100))
        screen.draw.line((80, 100, 148, 50))
        screen.draw.arc((30, 30, 90, 70), 180, 0)
        screen.draw.arc((90, 30, 148, 70), 180, 0)
        screen.update()
        Sound.speak("Heart")
    elif y_new[0] == 1:
        screen.clear()
        lines = [(80,20),(20,100),(158,100)]
        screen.draw.polygon(lines)
        screen.update()
        Sound.speak("Triangle")


run()
