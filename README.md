# 🍱 Lunch Menu Slack Notifier

> **사내 점심 식단을 슬랙으로 자동 공유하세요.**  
> 이 프로젝트는 SK 하이닉스 사내 식당 API에서 점심 메뉴를 수집하여  
> 매일 아침 Slack 채널로 자동 전송하는 Python 기반 자동화 스크립트입니다.

---

## 📌 프로젝트 개요

- 매일 수동으로 식단을 확인하는 번거로움을 제거
- 캠퍼스/식당/식사 유형별 메뉴 자동 파싱
- Slack Webhook을 활용한 깔끔한 메시지 전송
- Windows 작업 스케줄러를 통한 완전 자동화

---

## ✨ 주요 기능

- **🔍 정밀 메뉴 파싱**  
  캠퍼스 코드, 식당 번호, 식사 타입을 기준으로 정확한 메뉴만 추출합니다.

- **📅 워킹데이 자동 판단**  
  토·일요일에는 자동으로 실행을 종료하여 불필요한 알림을 방지합니다.

- **🔒 사내 SSL 환경 대응**  
  사내 보안망에서 자주 발생하는 SSL 인증서 오류를 감지하여  
  `verify=False` 모드로 안전하게 우회 처리합니다.

- **🎨 Slack 리치 메시지 포맷**  
  단순 텍스트가 아닌 `attachments` 기반 메시지로 가독성을 높였습니다.

- **📝 상세 로그 관리**  
  정상 실행 로그와 에러 로그를 분리 저장하여 트러블슈팅이 용이합니다.

---

## 🛠 기술 스택

| 구분 | 내용 |
|---|---|
| Language | Python 3.8+ |
| Library | requests, python-dotenv, urllib3 |
| Automation | Windows Task Scheduler |
| Messaging | Slack Incoming Webhook |

---

## 🚀 시작하기

### 1️⃣ 필수 라이브러리 설치

```bash
pip install requests python-dotenv urllib3
```

---

### 2️⃣ 환경 변수 설정

프로젝트 루트 디렉터리에 `.env` 파일을 생성하고 아래 내용을 입력합니다.

```env
# API & Slack
MENU_URL=https://example.com/api/menu
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXX/XXXX/XXXX

# 식당 정보
CAMPUS=ICHON
CAFETERIA_SEQ=21
MEAL_TYPE=LN
```

> ⚠️ `.env` 파일은 외부에 노출되지 않도록 반드시 관리하세요.

---

## ⏰ Windows 작업 스케줄러 설정

매일 자동으로 식단을 수신하려면 아래와 같이 설정합니다.

### 🔹 기본 설정

1. 시작 메뉴 → **작업 스케줄러** 실행  
2. **기본 작업 만들기** 선택  
3. 이름: `Daily_Lunch_Bot`

### 🔹 트리거

- 실행 주기: **매일**
- 권장 시간: **오전 10:30**

### 🔹 동작

- 동작: **프로그램 시작**

| 설정 항목 | 예시 값 | 설명 |
|---|---|---|
| 프로그램/스크립트 | `C:\Python39\python.exe` | Python 실행 경로 |
| 인수 추가 | `C:\Scripts\lunch_bot\main.py` | 실행할 스크립트 |
| 시작 위치 | `C:\Scripts\lunch_bot\` | `.env` 로드 필수 |

---

## 🗂 프로젝트 구조

```plaintext
.
├── main.py             # 메인 실행 및 파싱 로직
├── .env                # 환경 변수 설정 파일 (외부 공유 금지)
├── lunch_debug.log     # 정상 실행 로그
└── lunch_error.log     # 에러 로그
```

---

## 💡 주의 사항

- **시작 위치 누락 주의**  
  작업 스케줄러에서 시작 위치를 지정하지 않으면 `.env` 파일을 찾지 못합니다.

- **SSL 인증서 경고**  
  사내망 특성상 SSL 경고가 발생할 수 있으나,  
  `urllib3.disable_warnings()`로 안전하게 처리합니다.

- **문제 발생 시**  
  실행 실패 시 `lunch_error.log`를 가장 먼저 확인하세요.

---

## 📄 라이선스

This project is licensed under the **MIT License**.
