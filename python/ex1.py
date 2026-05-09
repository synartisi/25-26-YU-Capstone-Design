import serial
import pandas as pd
import time

# 1. 시리얼 포트 설정 (사용자의 환경에 맞게 'COM3' 등을 수정하세요)
PORT = "COM3"
BAUD_RATE = 9600
TIMEOUT = 1


def process_motion_data(df, window_size=5):
    """사용자가 제공한 가공 로직 (최적화 버전)"""
    # 이동 평균 계산
    df["roll_sma"] = df["roll"].rolling(window=window_size).mean()
    df["pitch_sma"] = df["pitch"].rolling(window=window_size).mean()
    df["yaw_sma"] = df["yaw"].rolling(window=window_size).mean()

    # 변화율(차분) 계산
    df["pitching_rate"] = df["pitch"].diff()
    df["yawing_rate"] = df["yaw"].diff()

    # 결측치 제거
    return df.dropna()


def main():
    try:
        # 시리얼 연결
        ser = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"Connected to {PORT}...")

        raw_records = []  # 수집된 데이터를 담을 리스트

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8").strip()

                # 데이터 파싱 (CSV 형태: roll,pitch,yaw,flex)
                try:
                    parts = line.split(",")
                    if len(parts) == 4:
                        # 숫자 데이터로 변환
                        record = {
                            "roll": float(parts[0]),
                            "pitch": float(parts[1]),
                            "yaw": float(parts[2]),
                            "flex": float(parts[3]),
                        }
                        raw_records.append(record)

                        # 화면에 현재 수집 상황 출력 (선택 사항)
                        print(f"Captured: {record}", end="\r")

                        # 2. 데이터가 어느 정도 쌓이면(예: 30개) 가공 로직 실행
                        if len(raw_records) >= 30:
                            df = pd.DataFrame(raw_records)
                            processed_df = process_motion_data(df, window_size=5)

                            print("\n\n--- [가공된 데이터 최신 5행] ---")
                            print(processed_df.tail(5))
                            print("-------------------------------\n")

                            # (선택) 데이터를 저장하거나 리스트를 비움
                            # raw_records = [] # 계속 누적하려면 주석 처리

                except ValueError:
                    # 데이터가 깨져서 들어오는 경우 무시
                    continue

    except KeyboardInterrupt:
        print("\n수집 중단. 프로그램을 종료합니다.")
    except Exception as e:
        print(f"\n에러 발생: {e}")
    finally:
        if "ser" in locals() and ser.is_open:
            ser.close()


if __name__ == "__main__":
    main()
