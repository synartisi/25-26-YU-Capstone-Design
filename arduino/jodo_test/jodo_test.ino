int cdsPin = A0;   // 조도센서 모듈 A0 연결
int ledPin = 13;   // LED 연결

void setup() {
  Serial.begin(9600);    
  pinMode(ledPin, OUTPUT);
}

void loop() {
  int cdsValue = analogRead(cdsPin); // 센서 값 읽기
  
  Serial.print("Light Value: ");
  Serial.println(cdsValue);

  // 보통 모듈형은 어두워지면 값이 커지는 경향이 있습니다.
  // 시리얼 모니터로 값을 확인한 후 아래 부등호와 기준값을 조정하세요.
  if (cdsValue > 400) {      // 예시: 값이 400보다 커지면(어두워지면) LED ON
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }

  delay(200); 
}
