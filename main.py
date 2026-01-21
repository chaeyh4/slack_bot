import requests
import datetime
import re
import json
import urllib3
import os
from requests.exceptions import SSLError
from dotenv import load_dotenv
from datetime import timezone, timedelta

# =========================
# 공통 로그 함수
# =========================
def log(msg: str):
    print(msg)
    with open("lunch_debug.log", "a", encoding="utf-8") as f:
        f.write(msg + "\n")

# =========================
# .env 로드 (로컬용)
# =========================
load_dotenv()

MENU_URL = os.getenv("MENU_URL")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

CAMPUS = os.getenv("CAMPUS", "BD")
CAFETERIA_SEQ = os.getenv("CAFETERIA_SEQ", "21")
MEAL_TYPE = os.getenv("MEAL_TYPE", "LN")

if not MENU_URL or not SLACK_WEBHOOK_URL:
    raise RuntimeError("환경변수 에러")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =========================
# 시간 / 실행 조건
# =========================
KST = timezone(timedelta(hours=9))
now = datetime.datetime.now(KST)

log(f"[STEP 0] start time: {now.isoformat()}")
log(f"[STEP 0] weekday: {now.weekday()}")

IS_MANUAL = os.getenv("GITHUB_EVENT_NAME") == "workflow_dispatch"
log(f"[STEP 0] is_manual: {IS_MANUAL}")

if now.weekday() >= 5 and not IS_MANUAL:
    log("[EXIT] weekend and not manual")
    exit()

today = now.strftime("%Y%m%d")
log(f"[STEP 0] today (KST): {today}")

log(f"[STEP 0] MENU_URL exists: {bool(MENU_URL)}")
log(f"[STEP 0] SLACK_WEBHOOK_URL exists: {bool(SLACK_WEBHOOK_URL)}")

# =========================
# 요청 데이터
# =========================
payload = {
    "campus": CAMPUS,
    "cafeteriaSeq": CAFETERIA_SEQ,
    "mealType": MEAL_TYPE,
    "ymd": today
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    # =========================
    # 1. 메뉴 조회
    # =========================
    log("[STEP 1] requesting menu")

    try:
        res = requests.post(
            MENU_URL,
            data=payload,
            headers=headers,
            timeout=10
        )
    except SSLError as e:
        log(f"[STEP 1] SSL error, retry verify=False: {repr(e)}")
        res = requests.post(
            MENU_URL,
            data=payload,
            headers=headers,
            verify=False,
            timeout=10
        )

    log(f"[STEP 1] response status: {res.status_code}")
    res.raise_for_status()
    res.encoding = "utf-8"
    html = res.text

    log(f"[STEP 1] html length: {len(html)}")

    # =========================
    # 2. JSON 블록 추출
    # =========================
    menu_blocks = re.findall(r'\{[^{}]*"COURSE_NAME"[^{}]*\}', html)
    log(f"[STEP 2] menu_blocks count: {len(menu_blocks)}")

    if not menu_blocks:
        log("[EXIT] no menu_blocks found")
        exit()

    # =========================
    # 3. JSON 파싱
    # =========================
    menu_list = []

    for i, block in enumerate(menu_blocks):
        try:
            obj = json.loads(block)
            menu_list.append(obj)
        except json.JSONDecodeError as e:
            log(f"[STEP 2] JSON decode fail at block {i}: {e}")

    log(f"[STEP 2] menu_list count: {len(menu_list)}")

    if not menu_list:
        log("[EXIT] menu_list empty")
        exit()

    # =========================
    # 4. Slack 메시지 생성
    # =========================
    log("[STEP 3] building slack message")

    def extract_sides(menu):
        return [
            menu.get(f"SIDE_{i}")
            for i in range(1, 7)
            if menu.get(f"SIDE_{i}")
        ]

    lines = [f"🍱 오늘의 점심 메뉴 ({today})", ""]

    for menu in menu_list:
        lines.append(f"[{menu.get('COURSE_NAME', '')}] 🍽 {menu.get('MENU_NAME', '')}")
        for side in extract_sides(menu):
            lines.append(f"• {side}")
        lines.append("")

    slack_message = "\n".join(lines)

    log("[STEP 3] slack_message preview:")
    log(slack_message)

    # =========================
    # 5. Slack 전송
    # =========================
    log("[STEP 4] sending slack message")

    slack_res = requests.post(
        SLACK_WEBHOOK_URL,
        json={"message": slack_message},
        timeout=10
    )

    log(f"[STEP 4] slack response status: {slack_res.status_code}")
    slack_res.raise_for_status()

    log("[SUCCESS] slack message sent")

except Exception as e:
    log(f"[ERROR] {repr(e)}")
    log("[FAILURE] failed to send slack message")