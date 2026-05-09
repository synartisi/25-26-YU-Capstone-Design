import time
from adafruit_servokit import ServoKit

# 16채널 PCA9685 객체 생성
kit = ServoKit(channels=16)

# MG966R의 펄스 폭 범위 설정 (일반적으로 500~2500 사이, 모터마다 다를 수 있음)
# 0번 채널에 연결된 모터 설정
kit.servo[0].set_pulse_width_range(500, 2500)

while True:
    print("0도")
    kit.servo[0].angle = 0
    time.sleep(1)

    print("90도")
    kit.servo[0].angle = 90
    time.sleep(1)

    print("180도")
    kit.servo[0].angle = 180
    time.sleep(1)
