# SPDX-FileCopyrightText: 2026 코딩 파트너 for User Project
# SPDX-License-Identifier: MIT

import json
import serial
import time
import paho.mqtt.client as mqtt

# ==========================================
# 1. 환경 및 통신 설정
# ==========================================
MQTT_BROKER = "localhost"  # 라즈베리파이 내부 브로커 사용
MQTT_TOPIC = "robot/glove/sensors"

try:
    ser = serial.Serial("/dev/rfcomm0", 9600, timeout=1)
    print("🚀 [성공] 블루투스 장치와 연결되었습니다. (/dev/rfcomm0)")
except Exception as e:
    print(f"❌ [오류] 블루투스 포트 개방 실패: {e}")
    exit()

# MQTT 클라이언트 초기화
mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
try:
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_start()
    print("📡 [성공] MQTT 브로커에 연결되었습니다.")
except Exception as e:
    print(f"❌ [오류] MQTT 브로커 연결 실패: {e}")
    exit()


def calculate_xor_checksum(data_string):
    """아두이노의 XOR 체크섬과 동일하게 문자열의 각 문자 ASCII 값을 XOR 연산합니다."""
    checksum = 0
    for char in data_string:
        checksum ^= ord(char)
    return checksum


# ==========================================
# 2. 메인 수신 및 발행(Publish) 루프
# ==========================================
try:
    while True:
        if ser.in_waiting > 0:
            try:
                raw_bytes = ser.readline()
                raw_data = raw_bytes.decode("utf-8", errors="ignore").rstrip()

                if not raw_data:
                    continue

                if "," in raw_data:
                    parts = raw_data.rsplit(",", 1)
                    if len(parts) != 2:
                        continue

                    data_part_str = parts[0]
                    received_checksum_str = parts[1]

                    # 체크섬 검증
                    arduino_style_string = data_part_str + ","
                    calculated_checksum = calculate_xor_checksum(
                        arduino_style_string
                    )

                    try:
                        received_checksum = int(received_checksum_str)
                    except ValueError:
                        continue

                    # [검증 완료] 데이터를 파싱 후 JSON 형태로 Pub 수행
                    if calculated_checksum == received_checksum:
                        value_list = data_part_str.split(",")

                        if len(value_list) == 4:
                            # 가독성과 확장성을 위해 JSON 구조로 매핑
                            sensor_data = {
                                "roll": int(value_list[0]),
                                "pitch": int(value_list[1]),
                                "yaw": int(value_list[2]),
                                "flex": int(value_list[3]),
                                "timestamp": time.time(),
                            }

                            # 객체를 문자열로 직렬화하여 특정 토픽으로 발행(Publish)
                            mqtt_client.publish(
                                MQTT_TOPIC, json.dumps(sensor_data)
                            )
                            print(f"📤 [Pub] {sensor_data}")

            except Exception as e:
                print(f"🔥 게이트웨이 루프 에러: {e}")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n👋 게이트웨이가 안전하게 종료됩니다.")
finally:
    ser.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
