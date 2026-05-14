import serial

# 바인딩된 포트 연결
ser = serial.Serial("/dev/rfcomm0", 9600)

while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode("utf-8").rstrip()
        print(f"아두이노로부터 온 데이터: {data}")
