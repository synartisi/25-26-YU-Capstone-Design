#include <SoftwareSerial.h>

SoftwareSerial imuSerial(2, 3); // 2번: RX (CVBE-010의 TXD), 3번: TX (CVBE-010의 RXD) ++ 아두이노 보드의 TX RX 핀사용하면 안된다고 함.
SoftwareSerial btSerial(10, 11); 

// WT901C485 축 기준: X=Roll(좌우), Y=Pitch(앞뒤), Z=Yaw(방향)

// Modbus 요청 패킷 (롤링, 피칭, 요잉)
byte requestAngle[] = {0x50, 0x03, 0x00, 0x3D, 0x00, 0x03, 0x99, 0x86}; 

unsigned char rxBuffer[11];
int bufferIndex = 0;

void setup() {
  Serial.begin(9600);
  imuSerial.begin(9600); // 센서 기본 통신 속도
  Serial.println("WT901C485 Modbus Angle Reader Start!");
}

void loop() {
  // 1. 센서에 Data 요청
  imuSerial.write(requestAngle, 8);
  delay(50); // Sensor Response step

  bufferIndex = 0;
  // 2. Response Data 버퍼에 채우기
  while (imuSerial.available()) {
    if (bufferIndex < 11) {
      rxBuffer[bufferIndex++] = imuSerial.read();
    } else {
      imuSerial.read(); // error(diff) 처리
    }
  }

  // 3. 정상적인 Modbus 응답 길이(11바이트)를 받았는지 확인
  if (bufferIndex == 11 && rxBuffer[0] == 0x50 && rxBuffer[1] == 0x03) {
    
    // 2바이트씩 묶어서 16비트 정수(short)로 변환 (음수 처리를 위해 short 사용)
    short rollRaw  = (rxBuffer[3] << 8) | rxBuffer[4];
    short pitchRaw = (rxBuffer[5] << 8) | rxBuffer[6];
    short yawRaw   = (rxBuffer[7] << 8) | rxBuffer[8];

    // 공식 대입하여 각도(Degree)로 환산
    float roll  = (float)rollRaw / 32768.0 * 180.0;
    float pitch = (float)pitchRaw / 32768.0 * 180.0;
    float yaw   = (float)yawRaw / 32768.0 * 180.0;

    // Serial Monitor
    Serial.print("Roll: "); Serial.print(roll, 2);
    Serial.print(" | Pitch: "); Serial.print(pitch, 2);
    Serial.print(" | Yaw: "); Serial.println(yaw, 2);
    
  } else {
    Serial.println("Waiting for valid data packet...");
  }

  delay(100); // time step = 1 sec
}
