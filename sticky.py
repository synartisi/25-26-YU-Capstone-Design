import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
import time

i2c = board.I2C()
pca = PCA9685(i2c)
pca.frequency = 50
servo7 = servo.Servo(pca.channels[4])

# 서보를 0도로 이동시키고 고정!
print("Setting servo to 0 degrees...")
servo7.angle = 0

# 이 상태에서 프로그램을 종료하지 말고 그대로 둡니다.
# 모터가 "지잉" 소리를 내며 0도 위치를 꽉 잡고 있을 겁니다.
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
