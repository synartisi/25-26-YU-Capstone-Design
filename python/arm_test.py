import serial
import time
from adafruit_servokit import ServoKit

# 1. 하드웨어 및 라이브러리 초기화
try:
    kit = ServoKit(channels=16)
    # MG996R 특성에 맞춘 펄스 범위 설정 (부들부들 떨리면 750, 2250으로 조절)
    for i in range(3):
        kit.servo[i].set_pulse_width_range(500, 2500)
    print("PCA9685 Initialized.")
except Exception as e:
    print(f"I2C Error: {e}\n'sudo i2cdetect -y 1'로 0x40 주소를 확인하세요.")
    exit()

# 블루투스 시리얼 포트 설정
try:
    bt_serial = serial.Serial("/dev/rfcomm0", 9600, timeout=1)
    print("Bluetooth Serial Connected! (/dev/rfcomm0)")
except Exception as e:
    print(f"Bluetooth Error: {e}\n'sudo rfcomm bind' 상태를 확인하세요.")
    exit()

# 2. 제어 변수 설정
alpha = 0.3  # 필터 강도 (1.0에 가까울수록 반응은 빠르나 떨림이 심해짐)
smooth_y, smooth_p, smooth_r = 90.0, 90.0, 90.0
offset_y, offset_p, offset_r = 0.0, 0.0, 0.0
is_calibrated = False


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


# ---------------------------------------------------------
# 초기 데이터 확인 및 영점 조정 대기
# ---------------------------------------------------------
print("\n[Step 1] Checking incoming data...")
time.sleep(1)

print("[Step 2] Move IMU to your 'Center' position.")
print("[Step 3] Press Enter to Calibrate and Start Control!")
input()  # 사용자가 엔터를 누를 때까지 대기

# 3. 메인 제어 루프
try:
    while True:
        if bt_serial.in_waiting > 0:
            # 데이터 한 줄 읽기
            line = bt_serial.readline().decode("utf-8", errors="ignore").strip()

            # [디버깅] 원본 데이터 출력
            print(f"Raw Data: {line}")

            parts = line.split(",")
            if len(parts) == 3:
                try:
                    # 데이터 파싱 (아두이노 송신 순서: roll, pitch, yaw)
                    curr_r, curr_p, curr_y = map(float, parts)

                    # 영점 보정 (엔터 누른 시점의 값을 0으로 간주)
                    if not is_calibrated:
                        offset_r, offset_p, offset_y = curr_r, curr_p, curr_y
                        is_calibrated = True
                        print(">>> Calibration Done! Control Started.")
                        continue

                    # 1. 오프셋 적용 및 타겟 각도 계산 (중심 90도)
                    target_r = (curr_r - offset_r) + 90
                    target_p = (curr_p - offset_p) + 90
                    target_y = (curr_y - offset_y) + 90

                    # 2. 지수 이동 평균(EMA) 필터로 부드럽게 변환
                    smooth_r = (alpha * target_r) + (1.0 - alpha) * smooth_r
                    smooth_p = (alpha * target_p) + (1.0 - alpha) * smooth_p
                    smooth_y = (alpha * target_y) + (1.0 - alpha) * smooth_y

                    # 3. 서보 모터에 각도 명령 전달 (범위 제한 포함)
                    kit.servo[0].angle = constrain(smooth_y, 0, 180)  # Base
                    kit.servo[1].angle = constrain(smooth_p, 0, 180)  # Shoulder
                    kit.servo[2].angle = constrain(smooth_r, 0, 180)  # Wrist

                    # [디버깅] 계산된 타겟 각도 출력
                    print(
                        f"Target -> Y:{smooth_y:6.1f} | P:{smooth_p:6.1f} | R:{smooth_r:6.1f}"
                    )

                except ValueError:
                    print("Data Parsing Error (Skipping...)")
                    pass

except KeyboardInterrupt:
    print("\n[System] Stop Control. Closing Serial...")
    bt_serial.close()
