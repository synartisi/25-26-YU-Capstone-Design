# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board
from adafruit_motor import servo

from adafruit_pca9685 import PCA9685

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)
# You can optionally provide a finer tuned reference clock speed to improve the accuracy of the
# timing pulses. This calibration will be specific to each board and its environment. See the
# calibration.py example in the PCA9685 driver.
# pca = PCA9685(i2c, reference_clock_speed=25630710)
pca.frequency = 50

# To get the full range of the servo you will likely need to adjust the min_pulse and max_pulse to
# match the stall points of the servo.
# This is an example for the Sub-micro servo: https://www.adafruit.com/product/2201
# servo7 = servo.Servo(pca.channels[7], min_pulse=580, max_pulse=2350)
# This is an example for the Micro Servo - High Powered, High Torque Metal Gear:
#   https://www.adafruit.com/product/2307
# servo7 = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2600)
# This is an example for the Standard servo - TowerPro SG-5010 - 5010:
#   https://www.adafruit.com/product/155
# servo7 = servo.Servo(pca.channels[7], min_pulse=400, max_pulse=2400)
# This is an example for the Analog Feedback Servo: https://www.adafruit.com/product/1404
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2500)
# This is an example for the Micro servo - TowerPro SG-92R: https://www.adafruit.com/product/169
# servo7 = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2400)

# The pulse range is 750 - 2250 by default. This range typically gives 135 degrees of
# range, but the default is to use 180 degrees. You can specify the expected range if you wish:
# servo7 = servo.Servo(pca.channels[7], actuation_range=135)
servo7 = servo.Servo(pca.channels[4])

# We sleep in the loops to give the servo time to move into position.
boundary = 130
for i in range(boundary):
    servo7.angle = i
    time.sleep(0.03)
for i in range(boundary):
    servo7.angle = 180 - i
    time.sleep(0.03)

# You can also specify the movement fractionally.
fraction = 0.0
while fraction < 1.0:
    servo7.fraction = fraction
    fraction += 0.01
    time.sleep(0.03)

# servo7.angle = None

#pca.deinit()
"""
# ... (기존 코드 생략)

# 1. fraction 루프가 끝나면 이미 약 180도 근처에 도달합니다.
# 하지만 확실하게 180도로 고정합니다.
print("Moving to 180 degrees...")
servo7.angle = 180
time.sleep(1.0)  # 180도로 이동할 시간을 충분히 줍니다.

# 2. 코드가 끝나기 전 0도로 이동합니다.
print("Returning to 0 degrees before exit...")
servo7.angle = 0
time.sleep(1.0)  # 0도로 돌아갈 시간을 줍니다.
"""
# PCA9685 인스턴스를 깔끔하게 종료하려면 주석을 해제하는 것이 좋습니다.
# pca.deinit()
