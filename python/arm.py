import serial
import time
from adafruit_servokit import ServoKit

# 1. 하드웨어 설정
# PCA9685 서보 드라이버 (I2C 연결)
kit = ServoKit(channels=16)

# 블루투스 시리얼 포트 설정
# sudo cat이 가능하므로 포트명은 '/dev/rfcomm0'입니다.
try:
    bt_serial = serial.Serial("/dev/rfcomm0", 9600, timeout=1)
    print("Bluetooth IMU Connected!")
except Exception as e:
    print(f"Connection Error: {e}")
    exit()

# 2. 제어 및 필터 변수
alpha = 0.2  # 값의 급격한 변화를 막는 필터 (0.1 ~ 0.5)
smooth_y, smooth_p, smooth_r = 90.0, 90.0, 90.0
offset_y, offset_p, offset_r = 0.0, 0.0, 0.0
is_calibrated = False


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


print("Reading Data... Press 'c' to Calibrate current position as Center.")

# 3. 메인 제어 루프
try:
    while True:
        if bt_serial.in_waiting > 0:
            # 한 줄 읽기 (예: "10.50,20.10,-5.00")
            line = bt_serial.readline().decode("utf-8", errors="ignore").strip()
            parts = line.split(",")

            if len(parts) == 3:
                try:
                    # 데이터 파싱
                    curr_r, curr_p, curr_y = map(float, parts)

                    # 처음 한 번은 현재 각도를 0(90도)으로 맞춤
                    if not is_calibrated:
                        offset_r, offset_p, offset_y = curr_r, curr_p, curr_y
                        is_calibrated = True
                        print("Calibration Done!")
                        continue

                    # 영점 보정 및 중심(90도) 이동
                    # 사람 팔의 움직임을 로봇 각도 범위(0~180)로 매핑
                    target_y = (curr_y - offset_y) + 90
                    target_p = (curr_p - offset_p) + 90
                    target_r = (curr_r - offset_r) + 90

                    # 부드러운 움직임을 위한 지수 이동 평균(EMA) 필터
                    smooth_y = (alpha * target_y) + (1.0 - alpha) * smooth_y
                    smooth_p = (alpha * target_p) + (1.0 - alpha) * smooth_p
                    smooth_r = (alpha * target_r) + (1.0 - alpha) * smooth_r

                    # 서보 모터 각도 전송 (채널 번호는 배선에 맞게 수정)
                    kit.servo[0].angle = constrain(smooth_y, 0, 180)  # Base (Yaw)
                    kit.servo[1].angle = constrain(smooth_p, 0, 180)  # Shoulder (Pitch)
                    kit.servo[2].angle = constrain(smooth_r, 0, 180)  # Wrist (Roll)

                    # 디버깅 출력
                    # print(f"Y:{smooth_y:.1f} P:{smooth_p:.1f} R:{smooth_r:.1f}")

                except ValueError:
                    pass  # 깨진 데이터 무시

except KeyboardInterrupt:
    print("\nStop Control.")
    bt_serial.close()
