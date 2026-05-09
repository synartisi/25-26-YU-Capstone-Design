#include <SoftwareSerial.h>

// [설정] 핀 번호 및 통신 설정
const int flexPin = A0;         // 밴딩 센서
SoftwareSerial imuSerial(2, 3); // IMU 센서 (2: RX, 3: TX)

// [설정] Modbus 요청 패킷
byte requestAngle[] = {0x50, 0x03, 0x00, 0x3D, 0x00, 0x03, 0x99, 0x86}; 
unsigned char rxBuffer[11];

void setup() {
  // PC 전송 속도는 115200 -> 9600 (데이터 누락 방지)
  Serial.begin(9600); 
  // IMU 통신 속도는 센서 기본값인 9600
  imuSerial.begin(9600); 

  // 파이썬 Pandas에서 컬럼명으로 바로 쓸 수 있게 헤더 출력 (최초 1회)
  // Serial.println("roll,pitch,yaw,flex"); 
  // ↑ 만약 실시간 그래프 툴을 쓴다면 위 줄은 주석 처리하거나 빼셔도 됩니다.
}

void loop() {
  // 1. 밴딩 센서 읽기
  int flexValue = analogRead(flexPin);

  // 2. IMU 데이터 요청
  imuSerial.write(requestAngle, 8);
  delay(40); // 응답 대기 시간을 살짝 최적화 (50ms -> 40ms)

  int bufferIndex = 0;
  while (imuSerial.available()) {
    if (bufferIndex < 11) {
      rxBuffer[bufferIndex++] = imuSerial.read();
    } else {
      imuSerial.read();
    }
  }

  // 3. 데이터 파싱 및 출력 (CSV 형식: roll,pitch,yaw,flex)
  if (bufferIndex == 11 && rxBuffer[0] == 0x50 && rxBuffer[1] == 0x03) {
    // raw 데이터 복원
    short rollRaw  = (rxBuffer[3] << 8) | rxBuffer[4];
    short pitchRaw = (rxBuffer[5] << 8) | rxBuffer[6];
    short yawRaw   = (rxBuffer[7] << 8) | rxBuffer[8];

    // 각도 환산
    float roll  = (float)rollRaw / 32768.0 * 180.0;
    float pitch = (float)pitchRaw / 32768.0 * 180.0;
    float yaw   = (float)yawRaw / 32768.0 * 180.0;

    // --- 핵심: 파이썬이 읽기 좋은 CSV 형태 출력 ---
    Serial.print(roll, 2);    Serial.print(",");
    Serial.print(pitch, 2);   Serial.print(",");
    Serial.print(yaw, 2);     Serial.print(",");
    Serial.println(flexValue); // 마지막 값 출력 후 줄바꿈
    
  } else {
    // 에러 발생 시 파이썬이 숫자로 인식하지 않도록 공백이나 특정 값을 보낼 수 있으나,
    // 보통 실시간 처리에서는 에러 줄은 그냥 건너뛰도록 아무것도 출력하지 않는 게 깔끔합니다.
  }

  // 전체 루프 속도 (20Hz 정도로 설정: 50ms)
  // 위쪽 delay(40)과 합쳐져 약 50~60ms 주기로 데이터가 전송됩니다.
  delay(100); 
}
