# 🏠 제스처 인식 기반 스마트 룸 제어 시스템

AI + IoT + MQTT를 활용한 무선 비접촉 홈 오토메이션 프로젝트

## 📌 프로젝트 개요

손짓만으로 실내 디바이스(조명, 문, 음악)를 **무선으로** 제어할 수 있는 비접촉 스마트 룸 시스템입니다.

### 핵심 가치

- **편의성**: 손이 더러울 때, 멀리 있을 때도 기기 제어 가능
- **무선 IoT**: MQTT 프로토콜 기반 완전 무선 통신
- **위생성**: 스위치나 리모컨 접촉 없이 제어
- **직관성**: 자연스러운 제스처로 쉽게 조작
- **확장성**: 여러 디바이스 동시 제어 가능

## ✋ 제스처 매핑

| 제스처         | 기능 | 디바이스           |
| -------------- | ---- | ------------------ |
| ✊ 주먹        | 끄기 | LED 조명           |
| 🖐 손바닥 펴기 | 켜기 | LED 조명           |
| 👆 검지 1개    | 열기 | 문 (서보모터)      |
| ✌️ 브이 (2개)  | 닫기 | 문 (서보모터)      |
| 🤟 세 손가락   | 재생 | 음악 (피에조 부저) |
| 🖖 네 손가락   | 정지 | 음악 (피에조 부저) |

## 🛠️ 기술 스택

### AI/ML

- **MediaPipe Hands**: 손 랜드마크 인식 (21개 포인트)
- **제스처 분류기**: 실시간 제스처 인식
- **쿨다운 시스템**: 0.8초 간격으로 오인식 방지

### 하드웨어

- **라즈베리파이 4**: 제스처 인식, MQTT 클라이언트, 웹서버
- **ESP32**: Wi-Fi 통신, MQTT 클라이언트, 디바이스 제어
- **카메라 모듈**: 실시간 제스처 캡처
- **센서/액추에이터**:
  - LED (조명 시뮬레이션)
  - 서보모터 SG90 (문 제어)
  - 피에조 부저 (음악 재생 - 생일 축하 노래)

### 소프트웨어

- **백엔드**: Python 3.11, Flask API
- **프론트엔드**: HTML5, CSS3, JavaScript, Chart.js
- **IoT 통신**: MQTT (Mosquitto Broker)
- **무선 통신**: Wi-Fi (ESP32)
- **분석**: CSV 기반 로깅, 행동 패턴 분석

### 통신 프로토콜

- **MQTT**: 라즈베리파이 ↔ ESP32 (제어 명령)
- **HTTP/REST**: 웹 대시보드 ↔ Flask API (상태 조회)

## 🌐 시스템 아키텍처

```
┌─────────────────┐
│   사용자 제스처   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐       MQTT        ┌──────────────┐
│  라즈베리파이     │ ◄──────────────►  │    ESP32     │
│  - MediaPipe    │   (Wi-Fi 무선)     │ - Wi-Fi 내장 │
│  - Flask API    │                   │  - 디바이스   │
│  - MQTT Client  │                   │    제어      │
└────────┬────────┘                   └──────┬───────┘
         │                                   │
         │ HTTP                              │
         │                                   ▼
         ▼                            ┌──────────────┐
┌─────────────────┐                   │  LED, 서보,   │
│  웹 대시보드     │                    │  부저         │
│  - 실시간 상태   │                    └──────────────┘
│  - 통계 분석     │
└─────────────────┘
```

## 📦 설치 방법

### 1. 라즈베리파이 설정

#### 시스템 업데이트

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

#### 프로젝트 클론

```bash
cd ~
git clone https://github.com/your-username/smart-room-gesture.git
cd smart-room-gesture
```

#### Python 가상환경 생성

```bash
python3 -m venv venv
source venv/bin/activate
```

#### OpenCV 설치

```bash
sudo apt-get install python3-opencv -y
```

#### Python 라이브러리 설치

```bash
# MediaPipe (라즈베리파이용)
pip3 install mediapipe==0.10.18

# Flask 관련
pip3 install flask flask-cors

# MQTT 라이브러리 (구버전 추천)
pip3 install paho-mqtt==1.6.1

# 기타
pip3 install pyserial
```

#### MQTT Broker (Mosquitto) 설치

```bash
# Mosquitto 설치
sudo apt-get install -y mosquitto mosquitto-clients

# 자동 시작 설정
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# 상태 확인
sudo systemctl status mosquitto
```

#### Mosquitto 설정

```bash
# 설정 파일 편집
sudo nano /etc/mosquitto/mosquitto.conf
```

맨 아래에 추가:

```
listener 1883
allow_anonymous true
```

저장 후 재시작:

```bash
sudo systemctl restart mosquitto
```

#### MQTT 테스트

```bash
# 터미널 1 (구독)
mosquitto_sub -h localhost -t test/topic

# 터미널 2 (발행)
mosquitto_pub -h localhost -t test/topic -m "Hello MQTT!"
```

#### 이모지 폰트 설치 (대시보드용)

```bash
sudo apt-get install fonts-noto-color-emoji
```

---

### 2. ESP32 설정

#### Arduino IDE 설치 및 설정

1. **ESP32 보드 매니저 URL 추가**
   - Arduino IDE → File → Preferences
   - "Additional Board Manager URLs"에 추가:

```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

2. **ESP32 보드 설치**

   - Tools → Board → Boards Manager
   - "esp32" 검색 → "ESP32 by Espressif Systems" 설치

3. **라이브러리 설치**
   - Sketch → Include Library → Manage Libraries
   - **PubSubClient** (by Nick O'Leary) 설치
   - **ESP32Servo** (by Kevin Harrington) 설치

#### ESP32 코드 업로드

1. `arduino/smart_room_esp32.ino` 파일 열기
2. Wi-Fi 정보 수정:

```cpp
const char* ssid = "your_wifi_name";
const char* password = "your_wifi_password";
const char* mqtt_server = "라즈베리파이_IP";  // 예: 192.168.0.100
```

3. 보드 설정:

   - Tools → Board → ESP32 Dev Module
   - Tools → Port → (ESP32가 연결된 포트)

4. Upload 버튼 클릭

---

## 🔌 하드웨어 연결

### ESP32 회로도

```
LED:
- ESP32 GPIO 15 → LED (+) → 220Ω 저항 → GND

서보모터 (SG90):
- 빨강선 (VCC) → ESP32 VIN (5V)
- 갈색선 (GND) → ESP32 GND
- 주황선 (Signal) → ESP32 GPIO 18

피에조 부저:
- ESP32 GPIO 19 → 부저 (+)
- 부저 (-) → ESP32 GND

전원:
- ESP32 USB → 5V 전원 (USB 충전기 또는 컴퓨터)
```

### 핀 매핑

| 디바이스    | ESP32 핀  | 용도          |
| ----------- | --------- | ------------- |
| LED         | GPIO 15   | 조명 제어     |
| 서보모터    | GPIO 18   | 문 제어       |
| 피에조 부저 | GPIO 19   | 음악 재생     |
| VIN         | 5V        | 서보모터 전원 |
| GND         | 공통 접지 | 모든 디바이스 |

---

## 🚀 실행 방법

### 1. 네트워크 설정

**라즈베리파이와 ESP32를 같은 Wi-Fi에 연결!**

예: 핸드폰 핫스팟 사용 (2.4GHz 필수!)

#### 라즈베리파이 IP 확인:

예: `172.20.10.8`

#### ESP32 코드에 IP 입력:

```cpp
const char* mqtt_server = "172.20.10.8";
```

---

### 2. ESP32 실행

1. ESP32 전원 연결 (USB)
2. Serial Monitor 확인 (115200 baud)
3. 연결 확인:

```
WiFi connected!
IP address: 172.20.10.7
MQTT connected!
Subscribed to: smartroom/control
ESP32 Ready!
```

---

### 3. 라즈베리파이에서 Flask 서버 실행

```bash
# 가상환경 활성화
source venv/bin/activate

# 서버 실행
python3 app.py
```

**출력 확인:**

```
✅ MQTT connected to localhost:1883
📡 MQTT broker connected!
🎥 Camera thread started
✅ Server ready!
📡 API running on http://0.0.0.0:5000
```

---

### 4. 웹 대시보드 접속

라즈베리파이 브라우저에서:

```bash
chromium-browser dashboard.html
```

또는 파일 탐색기에서 `dashboard.html` 더블클릭!

---

### 5. 제스처 제어!

카메라 앞에서 제스처:

- ✊ 주먹 → LED 꺼짐
- 🖐 손바닥 → LED 켜짐
- 👆 검지 → 문 열림
- ✌️ 브이 → 문 닫힘
- 🤟 세 손가락 → 음악 재생
- 🖖 네 손가락 → 음악 정지

---

## 📁 프로젝트 구조

```
smart-room-gesture/
├── app.py                      # Flask API 서버
├── gesture_recognition.py      # 메인 제스처 인식
├── device_controller.py        # 디바이스 제어 로직 (통합)
├── mqtt_controller.py          # MQTT 통신 컨트롤러 ⭐ NEW
├── arduino_controller.py       # 아두이노 시리얼 통신 (레거시)
├── analytics.py                # 사용자 행동 분석
├── dashboard.html              # 실시간 제어 대시보드
├── analytics.html              # 통계 분석 대시보드
├── requirements.txt            # Python 의존성
├── gesture_log.csv             # 사용 로그 (자동 생성)
├── arduino/
│   ├── smart_room.ino          # 아두이노 스케치 (레거시)
│   └── smart_room_esp32.ino    # ESP32 스케치 ⭐ NEW
└── README.md
```

---

## 📊 주요 기능

### 실시간 제어 대시보드

- 실시간 제스처 인식 표시
- 현재 디바이스 상태 (LED, 문, 음악)
- 연결 상태 표시 (MQTT)
- 반응형 디자인

### 통계 분석 대시보드

- **제스처 사용 빈도**: 가장 많이 사용한 제스처 막대 그래프
- **디바이스 사용 통계**: 디바이스 제어 패턴 파이 차트
- **시간대별 사용 패턴**: 시간대별 활동 꺾은선 그래프
- **최근 활동 로그**: 타임스탬프 기반 행동 기록
- **요약 통계**: 총 제스처 수, 가장 많이 사용한 제스처/디바이스

### 사용자 행동 패턴 분석

- 모든 제스처 동작 자동 로깅
- CSV 기반 데이터 저장
- 실시간 통계 계산
- 개인화된 사용 인사이트

---

## 🎯 차별화 포인트

- **완전 무선 IoT**: MQTT 프로토콜 기반 무선 통신
- **능동적 제어**: 단순 센서 측정이 아닌 실제 디바이스 제어
- **AI 기반 인터랙션**: 지능형 제스처 인식
- **통합 대시보드**: 모니터링 + 제어 + 분석
- **실제 하드웨어 연동**: 시뮬레이션이 아닌 실제 구현
- **데이터 기반 인사이트**: 행동 패턴 분석
- **확장 가능한 아키텍처**: 여러 ESP32 동시 제어 가능

---

## 🎓 교육적 가치

### 습득 기술

- AI/ML 모델 통합 (MediaPipe)
- 실시간 이미지 처리 (OpenCV)
- IoT 통신 프로토콜 (MQTT)
- 무선 통신 시스템 설계
- 하드웨어-소프트웨어 통합
- REST API 설계
- 데이터 시각화 (Chart.js)
- 사용자 행동 분석

---

## 🐛 문제 해결

### 카메라 문제

```bash
# 카메라 테스트
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL'); cap.release()"
```

### MQTT 연결 문제

```bash
# Mosquitto 상태 확인
sudo systemctl status mosquitto

# 재시작
sudo systemctl restart mosquitto

# 테스트
mosquitto_sub -h localhost -t smartroom/#
```

### ESP32 연결 문제

- Wi-Fi가 **2.4GHz**인지 확인 (5GHz 안 됨!)
- 라즈베리파이와 **같은 네트워크**인지 확인
- MQTT 서버 IP가 **정확한지** 확인
- Serial Monitor에서 에러 메시지 확인

### paho-mqtt 버전 문제

```bash
# 구버전 사용 (추천)
pip3 uninstall paho-mqtt
pip3 install paho-mqtt==1.6.1
```

### 이모지가 안 보일 때

```bash
# 이모지 폰트 설치
sudo apt-get install fonts-noto-color-emoji

# 브라우저 재시작
```

### MediaPipe 설치 (라즈베리파이)

```bash
# Python 3.11 사용 (3.12+ 미지원)
pip3 install mediapipe==0.10.18
```

---

## 🔧 MQTT 토픽 구조

### 제어 명령 (Publish to ESP32)

**Topic**: `smartroom/control`

| 명령         | 기능      |
| ------------ | --------- |
| `LIGHT_ON`   | LED 켜기  |
| `LIGHT_OFF`  | LED 끄기  |
| `DOOR_OPEN`  | 문 열기   |
| `DOOR_CLOSE` | 문 닫기   |
| `MUSIC_PLAY` | 음악 재생 |
| `MUSIC_STOP` | 음악 정지 |

### 상태 응답 (Subscribe from ESP32)

**Topic**: `smartroom/status`

| 응답      | 의미         |
| --------- | ------------ |
| `LIGHT:1` | LED 켜짐     |
| `LIGHT:0` | LED 꺼짐     |
| `DOOR:1`  | 문 열림      |
| `DOOR:0`  | 문 닫힘      |
| `MUSIC:1` | 음악 재생 중 |
| `MUSIC:0` | 음악 정지    |

---
