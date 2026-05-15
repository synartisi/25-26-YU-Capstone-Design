# Raspberry PI OS 설명서

<small>25-26 캡스톤디자인</small>

---
# 라즈베리파이 OS는 최소 32GB SD카드에
# Raspberry Pi Imager를 이용해서 굽는걸 추천
---
# 0. 라즈베리파이 자체 설정
```bash
# 리눅스에서 제일 많이 쓸 명령어(최신 보안 패치등 OS 업데이트 및 업그레이드)
sudo apt update && sudo apt upgrade -y 	# 우분투 역시 동일 명령어 사용
# 처음에 들어가면 보통 한글이 깨집니다 □ 같은 두부가 나옴
sudo apt install fonts-nanum -y 	# 네이버 나눔폰트 설치
sudo fc-cache -fv 	# 설치한 폰트를 리눅스가 읽게 하기
# ssh I2c Serial Locale( ko_kr UTF-8 로 변경) 설정 변경
sudo raspi-config 	# 라즈베리파이 시스템 공식 콘솔 매니저 명령어
# etc... 램 cpu gpu 사용량 확인(== Windows 의 작업 관리자 역할)
sudo apt install btop 	# bash에 btop 타이밍 시 관리 가능
```
```
```
---

# 라즈베리파이에서 pigpio 소스코드 다운로드
```bash
# pigpio 소스코드 다운로드 (홈 디렉토리 기준)
cd ~
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
#컴파일 및 설치
make
sudo make install

```
---
# 3. 파이썬 가상환경 생성(라즈베리파이 OS 공식 권장)
```bash
python3 -m venv [.venv|원하는 가상환경 이름] # 라즈베리파이 4B 파이썬 == 3.13.5 버전
source [.venv|원하는가상환경이름]/bin/activate 	# 가상환경 실행
pip install numpy adafruit-circuitpython-servokit pyserial picamera2 pigpio pandas
```

"""현재까지 설치해본 라즈베리파이 파이썬 가상환경 의존성(==요구 라이브러리)
dependencies = ["numpy",
  "adafruit-circuitpython-servokit",
  "pyserial",
  "picamera2",
  "pigpio",
  "pandas"
"""

---
# Python 코드 만드는 법: 내장 코드 에디터 Thonny 사용
```bash
thonny [test.py|코드 파일 이름]
python [test.py|실행시키고 싶은 파일 이름]	# Python 코드 실행
# **꼭 source 가상환경이름/bin/activate 하고 실행시키기**
```
```

