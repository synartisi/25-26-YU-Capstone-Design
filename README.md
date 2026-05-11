# 🛠️ 25-26 기계공학 캡스톤디자인
**Yeungnam University | Mechanical Engineering**
---
### 프로젝트 소개
본 저장소는 영남대학교 기계공학부 기계공학전공(정창윤 교수님) 25-26 캡스톤디자인 프로젝트를 위한 공간입니다.\
2025-2026 Yeungnam University Mechanical Engineering Capstone Design
> **Distro support:** Rasberry Pi 5 8GB's Operating system Raspbian OS (Debian Distros)* is main.\
> **Used Programs:** 아두이노 IDE, VSCODE, Linux Terminal(bash:Gnome 내장 nano), LLMs(Google Gemini)..etc(추가 가능)
---
## Quick Install
> **Install Files:** Arduino(cpp) & Python

### How to Install (Windows)
1. Install [git bash](https://git-scm.com/install/windows)

```bash
git repo clone https://github.com/synartisi/YU-capstone-25-26.git
```

**따라하기:**
https://velog.io/@selenium/Git-Git-Bash-%EC%84%A4%EC%B9%98-Windows-OS

### Mac & Linux

```bash
git clone https://github.com/synartisi/25-26-YU-Capstone-Design.git && cd 25-26-YU-Capstone-Design
```


---
## Plan

### Robotics model and arduino Car model for Capstone
**Rasberry Pi 5 8GB, Arduino Mega 2560 Board, Arduino Nano Board, Arduino Uno Board and Custom boards**

**Note:** 
  1. 현재는 Rasberry Pi 5 대신 Raspberry Pi 4 + Raspbian PI OS 64 bit 를 설치해 사용 중
  2. WITMOTION WT901C485 9-IMU 센서 작동 확인 ✅
  3. 무선동기티칭펜던트 + Bus Servo Motor 관련 Arduino Board Uno board 작동 관련 문제 확인 완 ✅
    - MG996R servo 구동 확인 완 + 모터 전원 부족 문제 확인 ✅
  4. 구동부 차량 수령 확인 및 휠 구동 확인 완(by arduino 보드) ✅
  5. Arduino + HC-06 + IMU 데이터 블루투스 통신 with 라즈베리파이 통신 확인 ✅
  6. 라즈베리파이4 에서 python 을 이용하여 MG966R 서보 모터 5개 가동 확인 완 ✅/
     Install them
     ```bash
     sudo apt-get update
     sudo apt-get install -y python3-pip i2c-tools
     pip3 install adafruit-circuitpython-servokit
     ```
  7. 

---
## ***논문(포스터, 결과 보고서, 발표영상)*** 제출 및 프로젝트 마무리 기한(**Deadline**) : ~ 26-05-25
 ### 작업 중 작업 과정, 문제 발생, 시험 구동, 데이터 측정 등 최대한 많은 사진, 영상을 남겨주세요.
