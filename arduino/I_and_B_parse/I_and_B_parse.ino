#include <SoftwareSerial.h>

const int flexPin = A0;
SoftwareSerial imuSerial(2, 3);   // 2: RX, 3: TX
SoftwareSerial btSerial(10, 11); // 10: RX(HC-06 TX), 11: TX(HC-06 RX)

byte requestAngle[] = {0x50, 0x03, 0x00, 0x3D, 0x00, 0x03, 0x99, 0x86}; 
unsigned char rxBuffer[11];

void setup() {
  Serial.begin(9600); 
  imuSerial.begin(9600); 
  btSerial.begin(9600);
  
  // 시작 시 블루투스 포트를 기본 활성화
  btSerial.listen(); 
  Serial.println("System Ready...");
}

void loop() {
  int flexValue = analogRead(flexPin);

  // --- 1. IMU 데이터 읽기 모드로 전환 ---
  imuSerial.listen(); 
  imuSerial.write(requestAngle, 8);
  
  // 데이터가 들어올 때까지 잠시 대기 (최대 50ms)
  unsigned long startTime = millis();
  int bufferIndex = 0;
  
  while (millis() - startTime < 50) {
    if (imuSerial.available()) {
      if (bufferIndex < 11) {
        rxBuffer[bufferIndex++] = imuSerial.read();
      } else {
        imuSerial.read();
      }
    }
  }

  // --- 2. 데이터 처리 및 블루투스 전송 ---
  if (bufferIndex == 11 && rxBuffer[0] == 0x50 && rxBuffer[1] == 0x03) {
    short rollRaw  = (rxBuffer[3] << 8) | rxBuffer[4];
    short pitchRaw = (rxBuffer[5] << 8) | rxBuffer[6];
    short yawRaw   = (rxBuffer[7] << 8) | rxBuffer[8];

    float roll  = (float)rollRaw / 32768.0 * 180.0;
    float pitch = (float)pitchRaw / 32768.0 * 180.0;
    float yaw   = (float)yawRaw / 32768.0 * 180.0;

    // 블루투스로 전송 (보낼 때는 listen() 전환이 필요 없으나 안정성을 위해 바로 송신)
    btSerial.print(roll, 2);    btSerial.print(",");
    btSerial.print(pitch, 2);   btSerial.print(",");
    btSerial.print(yaw, 2);     btSerial.print(",");
    btSerial.println(flexValue); 

    // 시리얼 모니터 확인용
    Serial.print("BT Sent: "); Serial.println(roll);
  }

  // 전체 루프 속도 조절
  delay(100); 
}