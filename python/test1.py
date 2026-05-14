import time
from adafruit_servokit import ServoKit
# function : servo repeat
def rep(num, rad):
    kit.servo[num].angle = rad
    time.sleep(1)
    return

# 16채널 PCA9685 객체 생성
kit = ServoKit(channels=16)

# MG966R의 펄스 폭 범위 설정 (일반적으로 500~2500 사이, 모터마다 다를 수 있음)
# 0번 채널에 연결된 모터 설정
kit.servo[0].set_pulse_width_range(500, 2500)

while True:
    for _ in [0, 2, 4, 6, 8]:
        print("0도")
        rep(_, 0)

        print("90도")
        rep(_, 90)

        print("180도")
        rep(_, 180)
