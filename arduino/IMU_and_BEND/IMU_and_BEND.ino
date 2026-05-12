#include <SoftwareSerial.h>
// WT901C485 축 기준: X=Roll(좌우), Y=Pitch(앞뒤), Z=Yaw(방향)
// 1. 핀 설정
const int flexPin1 = A0;
const int flexPin2 = A1;         // 밴딩 센서 핀
SoftwareSerial imuSerial(2, 3); // IMU 센서 (2: RX, 3: TX)

// 2. Modbus 요청 패킷 (롤링, 피칭, 요잉)
byte requestAngle[] = {0x50, 0x03, 0x00, 0x3D, 0x00, 0x03, 0x99, 0x86}; 
unsigned char rxBuffer[11];

void setup() {
  // PC와의 시리얼 통신 (모니터링용)
  Serial.begin(9600); 
  // IMU 센서와의 통신 (SoftwareSerial)
  imuSerial.begin(9600); 
  
  Serial.println("--- Unified Sensor System Start ---");
  Serial.println("Flex Sensor (A0) + IMU (WT901C485)");
  delay(1000);
}

void loop() {
  // === [PART 1: 밴딩 센서 데이터 읽기] ===
  int flexValue1 = analogRead(flexPin1);
  int flexValue2 = analogRead(flexPin2);


  // === [PART 2: IMU 센서 데이터 요청 및 읽기] ===
  imuSerial.write(requestAngle, 8);
  delay(50); // 센서 응답 대기 시간

  int bufferIndex = 0;
  while (imuSerial.available()) {
    if (bufferIndex < 11) {
      rxBuffer[bufferIndex++] = imuSerial.read();
    } else {
      imuSerial.read(); // 버퍼 초과 데이터 폐기
    }
  }

  // === [PART 3: 통합 데이터 출력] ===
  
  // 1. IMU 데이터 처리 및 출력
  if (bufferIndex == 11 && rxBuffer[0] == 0x50 && rxBuffer[1] == 0x03) {
    short rollRaw  = (rxBuffer[3] << 8) | rxBuffer[4];
    short pitchRaw = (rxBuffer[5] << 8) | rxBuffer[6];
    short yawRaw   = (rxBuffer[7] << 8) | rxBuffer[8];

    float roll  = (float)rollRaw / 32768.0 * 180.0;
    float pitch = (float)pitchRaw / 32768.0 * 180.0;
    float yaw   = (float)yawRaw / 32768.0 * 180.0;

    Serial.print("[IMU] R:"); Serial.print(roll, 2);
    Serial.print(" P:"); Serial.print(pitch, 2);
    Serial.print(" Y:"); Serial.print(yaw, 2);
  } else {
    Serial.print("[IMU] Data Error or Waiting...");
  }

  // 2. 밴딩 센서 데이터 출력 (한 줄에 이어서 출력)
  Serial.print(" | [Flex] Value: ");
  Serial.print(flexValue1); Serial.print(", "); Serial.println(flexValue2);
  
  // 밴딩 센서 시각화 (간단한 바 그래프)
  Serial.print(" Graph: ");
  int visualValue1 = map(flexValue1, 400, 800, 0, 20);
  int visualValue2 = map(flexValue2, 400, 800, 0, 20); // 가독성을 위해 그래프 길이를 20으로 조절
  for (int i = 0; i < visualValue1; i++) Serial.print("-");
    Serial.println(">");
  Serial.print(" Graph: ");
  for (int i = 0; i < visualValue2; i++) Serial.print("-");
    Serial.println(">");

  // 전체 루프 주기 조절
  delay(2000); 
}
