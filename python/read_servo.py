import serial
import pandas as pd
import pigpio  # 서보 제어용
import time

# --- [설정] ---
# 라즈베리파이 블루투스 포트로 변경
PORT = "/dev/rfcomm0"
BAUD_RATE = 9600
SERVO_PIN = 18  # 서보모터 신호선(GPIO 18)

# pigpio 초기화
pi = pigpio.pi()


def main():
    try:
        # 1. 시리얼 연결
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {PORT}...")

        raw_records = []

        while True:
            if ser.in_waiting > 0:
                # 2. 실시간 라인 읽기 (cat /dev/rfcomm0과 동일한 데이터)
                line = ser.readline().decode("utf-8").strip()

                try:
                    parts = line.split(",")
                    if len(parts) == 4:
                        # 데이터 파싱
                        record = {
                            "roll": float(parts[0]),
                            "pitch": float(parts[1]),
                            "yaw": float(parts[2]),
                            "flex": float(parts[3]),
                        }
                        raw_records.append(record)

                        # --- [실시간 서보모터 적용 부분] ---
                        # 예: roll 값(-90 ~ 90)을 서보 각도(0 ~ 180)로 변환
                        # 아두이노에서 오는 데이터 범위에 맞춰 +90 부분을 수정하세요.
                        target_angle = record["roll"] + 90

                        # 각도를 펄스폭(500~2500)으로 변환하여 모터 구동
                        pulse = 500 + (target_angle / 180.0) * 2000
                        pi.set_servo_pulsewidth(SERVO_PIN, pulse)
                        # ----------------------------------

                        # 3. 기존 Pandas 가공 로직 (데이터가 쌓였을 때 실행)
                        if len(raw_records) >= 30:
                            df = pd.DataFrame(raw_records)

                            # 최근 5개 행에 대한 SMA(이동평균) 계산
                            df["roll_sma"] = df["roll"].rolling(window=5).mean()

                            print(
                                f"\rCurrent Roll: {record['roll']:.2f} | Servo: {target_angle:.2f}",
                                end="",
                            )

                            # 메모리 관리를 위해 너무 오래된 데이터는 삭제 (선택 사항)
                            if len(raw_records) > 100:
                                raw_records.pop(0)

                except ValueError:
                    continue

    except KeyboardInterrupt:
        print("\n종료합니다.")
    finally:
        pi.set_servo_pulsewidth(SERVO_PIN, 0)  # 서보 끄기
        pi.stop()
        if "ser" in locals():
            ser.close()


if __name__ == "__main__":
    main()
