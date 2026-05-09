#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// PCA9685 객체 생성 (기본 I2C 주소는 0x40입니다)
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// MG996R에 최적화된 설정값 (모터마다 미세하게 다를 수 있음)
#define SERVOMIN  150 // 0도일 때의 펄스 길이 (약 150)
#define SERVOMAX  600 // 180도일 때의 펄스 길이 (약 600)
#define USMIN  600    // 최소 마이크로초
#define USMAX  2400   // 최대 마이크로초
#define SERVO_FREQ 50 // 서보모터 동작 주파수 (표준 50Hz)

void setup() {
  Serial.begin(9600);
  Serial.println("PCA9685 MG996R Test 시작!");

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // 50Hz로 설정

  delay(10);
}

// 특정 채널의 서보모터를 원하는 각도로 움직이는 함수
void setServoAngle(uint8_t channel, int angle) {
  // 0~180도 값을 SERVOMIN~SERVOMAX 펄스 값으로 변환
  int pulse = map(angle, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(channel, 0, pulse);
  
  Serial.print("채널 "); Serial.print(channel);
  Serial.print("번 각도: "); Serial.println(angle);
}

void multi(int num, int rad, int time) {
  setServoAngle(num, rad);
  delay(time);
}


void loop() {
  // 0번 채널에 연결된 MG996R을 0도에서 180도까지 왕복
  
  // 0도 -> 180도 이동
  for (int angle = 0; angle <= 180; angle += 30) {
    multi(8, angle, 500);
    multi(6, angle, 500);
    multi(4, angle, 500);
    multi(2, angle, 500);
    multi(0, angle, 500);
  }

  // 180도 -> 0도 이동
  for (int angle = 180; angle >= 0; angle -= 30) {
    multi(8, angle, 500);
    multi(6, angle, 500);
    multi(4, angle, 500);
    multi(2, angle, 500);
    multi(0, angle, 500);
  }
}