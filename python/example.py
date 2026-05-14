import pandas as pd
import numpy as np


def process_motion_data(df, window_size=5):
    """
    롤링, 요잉, 피칭 가공 함수
    df: 'roll', 'pitch', 'yaw' 컬럼을 포함한 pandas DataFrame
    window_size: 이동 평균을 계산할 윈도우 크기
    """

    # 1. 롤링 (Rolling): 이동 평균 (Moving Average)
    # 데이터의 노이즈를 줄이고 추세를 파악함
    df["roll_roll"] = df["roll"].rolling(window=window_size).mean()
    df["pitch_roll"] = df["pitch"].rolling(window=window_size).mean()
    df["yaw_roll"] = df["yaw"].rolling(window=window_size).mean()

    # 2. 피칭 (Pitching): 차분 (Difference) 또는 기울기
    # 값이 얼마나 빠르게 변하는지 (속도)를 나타냄
    df["pitching_rate"] = df["pitch"].diff()

    # 3. 요잉 (Yawing): 회전 속도 (Angular Velocity)
    # yaw 데이터의 변화율을 나타냄 (1차 미분)
    df["yawing_rate"] = df["yaw"].diff()

    # 결측치 처리 (rolling으로 인한 NaN 제거)
    df.dropna(inplace=True)

    return df


# --- 사용 예시 ---
if __name__ == "__main__":
    # 가상의 센서 데이터 생성 (실제로는 API/DB에서 가져옴)
    data = {
        "roll": [10, 11, 10, 12, 13, 14, 15, 14],
        "pitch": [1, 2, 1, 3, 2, 4, 3, 5],
        "yaw": [0, 1, 2, 1, 3, 2, 4, 3],
    }
    df = pd.DataFrame(data)

    print("원본 데이터:")
    print(df)

    # 데이터 가공
    processed_df = process_motion_data(df, window_size=2)

    print("\n가공된 데이터 (롤링/요잉/피칭):")
    print(processed_df)
