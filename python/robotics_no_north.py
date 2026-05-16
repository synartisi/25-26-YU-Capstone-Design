# SPDX-FileCopyrightText: 2026 코딩 파트너 for User Project
# SPDX-License-Identifier: MIT

import time
import board
import serial
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

# ==========================================
# 1. 하드웨어 및 통신 초기화 설정
# ==========================================
try:
    ser = serial.Serial("/dev/rfcomm0", 9600, timeout=1)
    print("🚀 [성공] 블루투스 장치와 연결되었습니다. (/dev/rfcomm0)")
except Exception as e:
    print(f"❌ [오류] 블루투스 포트 개방 실패: {e}")
    print("팁: sudo rfcomm bind 명령이나 블루투스 페어링 상태를 점검하세요.")
    exit()

# PCA9685 I2C 및 서보모터 인스턴스 초기화
i2c = board.I2C()
pca = PCA9685(i2c)
pca.frequency = 50

# 로봇팔 서보모터 채널 할당
servo_gripper = servo.Servo(pca.channels[0])  # 채널 0: 집게 (Flex 센서 연동)
servo_joint1 = servo.Servo(pca.channels[1])  # 채널 1: 하부 관절 1 (xz평면 제어)
servo_joint2 = servo.Servo(pca.channels[2])  # 채널 2: 상부 관절 2 (xz평면 제어)
servo_base = servo.Servo(
    pca.channels[3]
)  # 채널 3: 시작 부분의 servo (수평 회전 제어) ★추가


# ==========================================
# 2. 데이터 변환 및 체크섬 헬퍼 함수
# ==========================================
def calculate_xor_checksum(data_string):
    """아두이노의 XOR 체크섬과 동일하게 문자열의 각 문자 ASCII 값을 XOR 연산합니다."""
    checksum = 0
    for char in data_string:
        checksum ^= ord(char)
    return checksum


def map_value(value, in_min, in_max, out_min, out_max):
    """입력값을 센서 범위에서 서보모터의 안전 가동 각도 범위로 선형 변환합니다."""
    if value < in_min:
        value = in_min
    if value > in_max:
        value = in_max

    mapped = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return float(mapped)


# ==========================================
# 3. 메인 파싱 및 모터 제어 루프
# ==========================================
print("💡 라즈베리파이 4-축 로봇팔 통합 제어 시스템 수신 대기 중...")

try:
    while True:
        if ser.in_waiting > 0:
            try:
                # 데이터 수신 및 디코딩
                raw_bytes = ser.readline()
                raw_data = raw_bytes.decode("utf-8", errors="ignore").rstrip()

                if not raw_data:
                    continue

                # 데이터부와 체크섬부 분리
                if "," in raw_data:
                    parts = raw_data.rsplit(",", 1)

                    if len(parts) != 2:
                        print("⚠️ 패킷 구조가 올바르지 않습니다.")
                        continue

                    data_part_str = parts[0]
                    received_checksum_str = parts[1]

                    # 아두이노 패킷의 마지막 쉼표 복원 후 체크섬 비교
                    arduino_style_string = data_part_str + ","
                    calculated_checksum = calculate_xor_checksum(arduino_style_string)

                    try:
                        received_checksum = int(received_checksum_str)
                    except ValueError:
                        print("⚠️ 수신된 체크sum 정수 변환 실패")
                        continue

                    # [최종 검증 완료] 데이터가 완벽할 때만 모터 구동 명령 수행
                    if calculated_checksum == received_checksum:
                        value_list = data_part_str.split(",")

                        if len(value_list) == 4:
                            roll = float(value_list[0])
                            pitch = float(value_list[1])
                            yaw = float(value_list[2])
                            flex = int(value_list[3])

                            # ------------------------------------------
                            # 💡 원격 로봇팔 구동을 위한 각도 계산 제어부
                            # ------------------------------------------

                            # 1. 밴딩(Flex) 센서 데이터를 이용한 집게 제어
                            gripper_angle = map_value(flex, 500, 800, 180.0, 0.0)
                            servo_gripper.angle = gripper_angle

                            # 2. IMU Pitch 각도를 이용한 수직 xz평면 로봇팔 제어
                            base_joint_angle = map_value(
                                pitch, -60.0, 60.0, 30.0, 150.0
                            )
                            joint1_angle = base_joint_angle
                            joint2_angle = 180.0 - base_joint_angle

                            # 3. IMU Yaw(또는 Roll) 각도를 이용한 '시작 부분의 servo(수평 회전)' 제어 ★추가
                            # 사용자가 몸이나 팔을 좌우로 회전하는 범위(예: -45도 ~ 45도)를 정의합니다.
                            # 정중앙(0도)일 때 로봇팔도 정중앙(90도)을 바라보도록 매핑합니다.
                            base_yaw_angle = map_value(yaw, -45.0, 45.0, 0.0, 180.0)

                            # 만약 팔 회전(Yaw) 대신 손목 비틀기(Roll)로 회전시키고 싶다면 아래 주석을 해제하세요.
                            # base_yaw_angle = map_value(roll, -60.0, 60.0, 0.0, 180.0)

                            # PCA9685 모듈을 통한 물리 서보모터 각도 출력
                            servo_joint1.angle = joint1_angle
                            servo_joint2.angle = joint2_angle
                            servo_base.angle = base_yaw_angle  # ★추가

                            # 콘솔 실시간 모니터링 출력 (시작 부분 servo 각도 추가)
                            print(
                                f"✅ [정상] R:{roll:5.1f} | P:{pitch:5.1f} | Y:{yaw:5.1f} | F:{flex:4d} "
                                f"➔ [모터] Base:{base_yaw_angle:5.1f}° | J1:{joint1_angle:5.1f}° | J2:{joint2_angle:5.1f}°"
                            )

                        else:
                            print("⚠️ 데이터 개수 불일치 (패킷 누실)")
                    else:
                        print(
                            f"❌ [체크섬 불일치] 계산: {calculated_checksum} != 수신: {received_checksum}"
                        )

            except Exception as loop_error:
                print(f"🔥 루프 내부 시스템 에러 발생: {loop_error}")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n👋 사용자에 의해 프로그램이 안전하게 종료되었습니다.")
finally:
    pca.deinit()
    print("🔒 PCA9685 인스턴스가 안전하게 닫혔습니다.")
