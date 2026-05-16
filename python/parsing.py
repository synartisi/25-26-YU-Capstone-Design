import serial

# 1. 블루투스 시리얼 포트 설정
# 통신이 일시적으로 끊겼을 때 무한 대기(Blocking)를 방지하기 위해 timeout을 1초로 설정합니다.
ser = serial.Serial("/dev/rfcomm0", 9600, timeout=1)


def calculate_xor_checksum(data_string):
    """
    아두이노의 XOR 체크섬과 동일하게 문자열의 각 문자 ASCII 값을 XOR 연산합니다.
    """
    checksum = 0
    for char in data_string:
        checksum ^= ord(char)  # ord() 함수로 문자를 ASCII 정수로 변환 후 XOR
    return checksum


print("🚀 라즈베리파이 수신 및 체크섬 검증 시스템을 시작합니다.")

while True:
    if ser.in_waiting > 0:
        try:
            # 2. 데이터 읽기 및 디코딩 (노이즈 문자열 무시)
            raw_bytes = ser.readline()
            raw_data = raw_bytes.decode("utf-8", errors="ignore").rstrip()

            if not raw_data:
                continue

            # 3. 데이터부와 체크섬부 분리
            # 예시 패킷: "12.34,-45.67,89.12,523,98" -> 맨 오른쪽 쉼표를 기준으로 1번만 쪼갭니다.
            if "," in raw_data:
                parts = raw_data.rsplit(",", 1)

                if len(parts) != 2:
                    print("⚠️ 패킷 구조가 올바르지 않습니다.")
                    continue

                data_part_str = parts[0]  # "12.34,-45.67,89.12,523"
                received_checksum_str = parts[1]  # "98"

                # 아두이노는 마지막 쉼표까지 포함해서 체크섬을 구했으므로 다시 쉼표를 더해줍니다.
                arduino_style_string = data_part_str + ","

                # 4. 체크섬 계산 및 비교
                calculated_checksum = calculate_xor_checksum(arduino_style_string)

                try:
                    received_checksum = int(received_checksum_str)
                except ValueError:
                    print("⚠️ 수신된 체크섬을 정수로 변환할 수 없습니다.")
                    continue

                # 5. 데이터 최종 검증 및 활용
                if calculated_checksum == received_checksum:
                    # 체크섬이 일치하면 데이터를 컴마 기준으로 파싱합니다.
                    value_list = data_part_str.split(",")

                    if len(value_list) == 4:
                        roll = float(value_list[0])
                        pitch = float(value_list[1])
                        yaw = float(value_list[2])
                        flex = int(value_list[3])

                        # [성공] 데이터를 안전하게 출력하고 변수에 저장합니다.
                        print(
                            f"✅ [정상] Roll: {roll:6.2f} | Pitch: {pitch:6.2f} | Yaw: {yaw:6.2f} | Flex: {flex:4d}"
                        )

                        # TODO: 여기에 PCA9685 서보모터 제어 함수나 KOA FC 명령 송신 로직을 연결하면 됩니다.

                    else:
                        print("⚠️ 데이터 개수가 일치하지 않습니다. (패킷 누실)")
                else:
                    print(
                        f"❌ [체크섬 오류] 계산값: {calculated_checksum} != 수신값: {received_checksum}"
                    )

        except Exception as e:
            # 예상치 못한 시스템 에러 발생 시 프로그램 종료 없이 에러 로그만 출력 후 다음 패킷 대기
            print(f"🔥 루프 내부 에러 발생: {e}")
