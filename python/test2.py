import time
from adafruit_servokit import ServoKit
# function : servo repeat
def rep(num, rad):
    kit.servo[num].angle = rad
    return

# 16채널 PCA9685 객체 생성
kit = ServoKit(channels=16)

# MG966R의 펄스 폭 범위 설정 (일반적으로 500~2500 사이, 모터마다 다를 수 있음)
# 0번 채널에 연결된 모터 설정
kit.servo[0].set_pulse_width_range(500, 2500)

while True:
    if x >= 0:
        for _ in [0, 90, 180]:
        print(f"{_} 도")
        print("0, 2, 4, 6, 8")
        rep(2, _)
        rep(6, _)
        time.sleep(1)
    else:
         for _ in [0, 90, 180]:
        print(f"{_} 도")
        print("0, 2, 4, 6, 8")
        rep(0, _)
        rep(4, _)
        rep(8, _)
        time.sleep(1)


        