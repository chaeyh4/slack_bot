# 🍱 Menu Slack Bot

> **사내 점심 식단을 슬랙으로 자동 공유하세요.**  
> 이 프로젝트는 SK 하이닉스 구내 식당 API에서 점심 메뉴를 수집하여  
> Slack 채널로 자동 전송하는 Python 기반 봇입니다.

---

## 📌 프로젝트 개요

- 매일 수동으로 식단을 확인하는 번거로움을 제거
- 캠퍼스/식사 유형별 메뉴 자동 파싱
- Slack Webhook을 활용한 깔끔한 메시지 전송
- Windows 작업 스케줄러를 통한 완전 자동화
- Slack App 명령어로 실시간 메뉴 조회 기능 제공

---

## ✨ 주요 기능

- **🔍 메뉴 코너별 안내**  
  캠퍼스 코드, 식사 타입을 기준으로 코너별 메뉴를 매일 아침 10시 30분에 안내합니다.

- **🤖 Slack App 명령어 지원**  
  `/menu` 명령어로 오늘/내일의 점심/저녁 메뉴를 조회할 수 있습니다.

- **📅 워킹데이 자동 판단**  
  주말에는 자동으로 실행을 종료하여 불필요한 알림을 방지합니다.

- **🔒 사내 SSL 환경 대응**  
  사내 보안망에서 자주 발생하는 SSL 인증서 오류를 우회 처리합니다.

- **📝 상세 로그 관리**  
  정상 실행 로그와 에러 로그를 분리 저장하여 트러블슈팅이 용이합니다.

---

## 🛠 기술 스택

| 구분 | 내용 |
|---|---|
| Language | Python 3.8+ |
| Library | requests, python-dotenv, urllib3, slack-sdk, slack_bolt |
| Automation | Windows Task Scheduler |
| Messaging | Slack Incoming Webhook |
| App | Slack App |

---

## 🚀 시작하기

### 🔹 필수 라이브러리 설치

```bash
pip install -r requirements.txt
```

---

### 🔹 환경 변수 설정

프로젝트 루트 디렉터리에 `.env` 파일을 생성하고 아래 내용을 입력합니다.

```env
# API & Slack
MENU_URL=https://example.com/api/menu

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXX/XXXX/XXXX

# 식당 정보
CAMPUS=BD 
CAFETERIA_SEQ=21
MEAL_TYPE=LN
```

> ⚠️ `.env` 파일은 외부에 노출되지 않도록 반드시 관리하세요.

---

## ⏰ Windows 작업 스케줄러 설정 (워크플로 기준 - main.py)

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

## 📱 ️Slack App 설정 (menu_bot.py)

Slack App을 사용하여 `/menu` 명령어로 메뉴를 조회할 수 있도록 설정합니다.

### 🔹 Slack App 생성 및 권한 설정
1. [Slack API: Your Apps](https://api.slack.com/apps) 접속
2. **Create New App** 클릭 → **From scratch** 선택
3. 앱 이름 및 워크스페이스 선택 후 생성
4. **OAuth & Permissions** → **Scopes** 섹션에서 다음 권한 추가
   - `commands`
   - `chat:write`
5. **Install App to Workspace** 클릭하여 앱 설치 및 토큰 발급

### 🔹 슬래시 커맨드 설정

1. **Slash Commands** → **Create New Command** 클릭
2. 명령어: `/menu`
3. 요청 URL: `https://yourdomain.com/menu` (socket mode 사용 시 무관)
4. 명령어 설명: "오늘/내일의 점심/저녁 메뉴를 조회합니다."

## ⚙️ 환경 변수 업데이트

`.env` 파일에 다음 항목 추가

```env
SLACK_BOT_TOKEN=xoxb-XXXXXXXX
SLACK_APP_TOKEN=xapp-XXXXXXXX
```

---
## 🍱 메뉴 파일 생성
`menu_build.py` 파일을 실행하여 메뉴 데이터를 생성합니다.
실행 기준의 today, tomorrow 메뉴 json 파일이 생성됩니다.
자동화 스케줄러에 등록하여 매일 아침 실행되도록 설정할 수 있습니다.

```bash
python menu_build.py
```

## 🏃‍♂️ Slack App 실행

Slack App을 실행하려면 `menu_bot.py` 파일을 실행합니다.

```bash
python menu_bot.py
```

## 🗂 프로젝트 구조

```plaintext
.
├── .env                # 환경 변수 설정 파일
├── requirements.txt    # 패키지 설치 파일
├── lunch_debug.log     # 정상 실행 로그
├── lunch_debug.log     # 정상 실행 로그
├── main.py             # 메인 실행 및 파싱 로직
├── menu_build.py       # 메뉴 데이터 저장
├── menu_bot.py         # 슬랙 봇 핸들러
└── menu_store.py       # 메뉴 메세지 파싱 및 전송
```

---

## 💡 주의 사항

- **시작 위치 누락 주의**  
  작업 스케줄러에서 시작 위치를 지정하지 않으면 `.env` 파일을 찾지 못합니다.

- **SSL 인증서 경고**  
  사내망 특성상 SSL 경고가 발생할 수 있으나,  
  `urllib3.disable_warnings()`로 안전하게 처리합니다.

- **문제 발생 시**  
  실행 실패 시 `lunch_error.log`를 확인해주세요.

- **라이브러리 호환성**  
  Python 및 라이브러리 버전을 맞추지 않으면 오류가 발생할 수 있습니다.

---

## 📄 라이선스

This project is licensed under the **MIT License**.
