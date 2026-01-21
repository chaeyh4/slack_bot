# menu_store.py

import requests
import datetime
import re
import json
import urllib3
import os
from requests.exceptions import SSLError
from datetime import timezone, timedelta
from dotenv import load_dotenv

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MENU_URL = os.getenv("MENU_URL")
CAMPUS = os.getenv("CAMPUS", "BD")
CAFETERIA_SEQ = os.getenv("CAFETERIA_SEQ", "21")

KST = timezone(timedelta(hours=9))

# =========================
# 내부 유틸
# =========================
def _fetch_menu_html(payload: dict) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.post(
            MENU_URL,
            data=payload,
            headers=headers,
            timeout=10
        )
    except SSLError:
        res = requests.post(
            MENU_URL,
            data=payload,
            headers=headers,
            verify=False,
            timeout=10
        )

    res.raise_for_status()
    res.encoding = "utf-8"
    return res.text


def _parse_menu(html: str) -> list[dict]:
    blocks = re.findall(r'\{[^{}]*"COURSE_NAME"[^{}]*\}', html)
    menus = []

    for block in blocks:
        try:
            menus.append(json.loads(block))
        except json.JSONDecodeError:
            continue

    return menus


def _build_menu_text(menu_list: list[dict], date_str: str, meal_kr: str) -> str:
    if not menu_list:
        return ""

    def extract_sides(menu):
        return [
            menu.get(f"SIDE_{i}")
            for i in range(1, 7)
            if menu.get(f"SIDE_{i}")
        ]

    lines = [f"🍱 {date_str} {meal_kr} 메뉴", ""]

    for menu in menu_list:
        lines.append(f"[{menu.get('COURSE_NAME', '')}] 🍽 {menu.get('MENU_NAME', '')}")
        for side in extract_sides(menu):
            lines.append(f"• {side}")
        lines.append("")

    return "\n".join(lines).strip()


# =========================
# 외부 인터페이스 (Slack 봇에서 사용)
# =========================
def get_menu(day: str, meal: str) -> str | None:
    """
    day: today | tomorrow
    meal: lunch | dinner
    """

    if not MENU_URL:
        raise RuntimeError("MENU_URL not set")

    meal_type_map = {
        "lunch": "LN",
        "dinner": "DN",
    }

    if meal not in meal_type_map:
        return None

    now = datetime.datetime.now(KST)
    target_date = now + datetime.timedelta(days=1 if day == "tomorrow" else 0)
    ymd = target_date.strftime("%Y%m%d")

    payload = {
        "campus": CAMPUS,
        "cafeteriaSeq": CAFETERIA_SEQ,
        "mealType": meal_type_map[meal],
        "ymd": ymd,
    }

    html = _fetch_menu_html(payload)
    menu_list = _parse_menu(html)

    if not menu_list:
        return None

    date_kr = "오늘" if day == "today" else "내일"
    meal_kr = "점심" if meal == "lunch" else "저녁"

    return _build_menu_text(menu_list, date_kr, meal_kr)
