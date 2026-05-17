# SPDX-FileCopyrightText: 2026 코딩 파트너 for User Project
# SPDX-License-Identifier: MIT

import json
import time
import board
import paho.mqtt.client as mqtt
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

# ==========================================
# 1. 하드웨어 및 MQTT 설정
# ==========================================
MQTT_BROKER = "localhost"
MQTT_TOPIC = "robot/glove/sensors"

# PCA9685 I2C 및 서보모터 인스턴스 초기화
i2c = board.I2C()
pca = PCA9685(i2c)
pca.frequency = 50

# 로봇팔 서보모터 채널 할당
servo_gripper = servo.Servo(pca.channels[14], min_pulse=503, max_pulse=2495)  # 채널 0: 집게
servo_joint1 = servo.Servo(pca.channels[8])  # 채널 1: 하부 관절 1
servo_joint2 = servo.Servo(pca.channels[4])  # 채널 2: 상부 관절 2
servo_joint3 = servo.Servo(pca.channels[0]) # 채널 0 : 바닥 회전

def map_value(value, in_min, in_max, out_min, out_max):
    """입력값을 센서 범위에서 서보모터의 안전 가동 각도 범위로 선형 변환합니다."""
    if value < in_min:
        value = in_min
    if value > in_max:
        value = in_max
    mapped = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return int(mapped)


# ==========================================
# 2. MQTT 구독(Subscribe) 콜백 정의
# ==========================================
def on_connect(client, userdata, flags, rc, properties=None):
    """브로커 연결 성공 시 호출되어 토픽을 구독합니다."""
    print(f"🔗 [구독 시작] MQTT 브로커에 연결되었습니다. 토픽: {MQTT_TOPIC}")
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """새로운 센서 데이터(Message)가 발행되면 호출되어 모터를 제어합니다."""
    try:
        # JSON 문자열을 파이썬 딕셔너리로 역직렬화
        payload = json.loads(msg.payload.decode("utf-8"))

        roll = payload["roll"]
        pitch = payload["pitch"]
        yaw = payload["yaw"]
        flex = payload["flex"]

        # ------------------------------------------
        # 💡 원격 로봇팔 구동을 위한 각도 계산 제어부
        # ------------------------------------------
        # 1. 밴딩(Flex) 센서 데이터를 이용한 집게 제어[cite: 3]
        gripper_angle = map_value(flex, 80, 300, 180, 0)
        servo_gripper.angle = gripper_angle

        # 2. IMU Pitch 각도를 이용한 수직 xz평면 로봇팔 제어[cite: 3]
        base_joint_angle = map_value(pitch, -60, 60, 30, 150)
        joint1_angle = base_joint_angle
        joint2_angle = 180.0 - base_joint_angle
        base_yaw_angle = map_value(yaw, -170, -70, 120, 180)
        joint3_angle = base_yaw_angle

        # 물리 서보모터 각도 출력[cite: 3]
        servo_joint1.angle = joint1_angle
        servo_joint2.angle = joint2_angle
        servo_joint3.angle = joint3_angle

        print(
                f"📥 [Sub 구동] Flex:{flex:4d}, Pitch:{pitch:5d}°, Yaw:{yaw:5d}° ➔ Gripper:{gripper_angle:5d}° | J1:{joint1_angle:5d}°| base : {joint3_angle:5d}° | yaw:{base_yaw_angle:5d}"
        )

    except Exception as e:
        print(f"⚠️ 데이터 처리 및 모터 구동 에러: {e}")


# ==========================================
# 3. MQTT 클라이언트 루프 실행
# ==========================================
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_BROKER, 1883, 60)
    # 네트워크 루프를 백그라운드 스레드에서 무한 실행하여 이벤트를 대기합니다.
    client.loop_forever()

except KeyboardInterrupt:
    print("\n👋 로봇팔 제어 시스템이 안전하게 종료됩니다.")
finally:
    pca.deinit()
    print("🔒 PCA9685 인스턴스가 안전하게 닫혔습니다.")
