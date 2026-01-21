import requests
import datetime
import re
import json
import urllib3
import os
from requests.exceptions import SSLError
from dotenv import load_dotenv
from datetime import timezone, timedelta

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MENU_URL = os.getenv("MENU_URL")
CAMPUS = os.getenv("CAMPUS", "BD")
CAFETERIA_SEQ = os.getenv("CAFETERIA_SEQ", "21")

KST = timezone(timedelta(hours=9))
today = datetime.datetime.now(KST)

def fetch_menu(ymd: str, meal_type: str):
    payload = {
        "campus": CAMPUS,
        "cafeteriaSeq": CAFETERIA_SEQ,
        "mealType": meal_type,
        "ymd": ymd
    }

    try:
        res = requests.post(MENU_URL, data=payload, timeout=10)
    except SSLError:
        res = requests.post(MENU_URL, data=payload, verify=False, timeout=10)

    res.raise_for_status()
    res.encoding = "utf-8"

    blocks = re.findall(r'\{[^{}]*"COURSE_NAME"[^{}]*\}', res.text)
    menus = []

    for block in blocks:
        try:
            menus.append(json.loads(block))
        except json.JSONDecodeError:
            continue

    return menus

def normalize(menus):
    result = []
    for m in menus:
        sides = [
            m.get(f"SIDE_{i}")
            for i in range(1, 7)
            if m.get(f"SIDE_{i}")
        ]
        result.append({
            "course": m.get("COURSE_NAME"),
            "menu": m.get("MENU_NAME"),
            "sides": sides
        })
    return result

store = {}

for day_offset, day_key in [(0, "today"), (1, "tomorrow")]:
    date = (today + datetime.timedelta(days=day_offset)).strftime("%Y%m%d")
    store[day_key] = {
        "lunch": normalize(fetch_menu(date, "LN")),
        "dinner": normalize(fetch_menu(date, "DN"))
    }

with open("menu_data.json", "w", encoding="utf-8") as f:
    json.dump(store, f, ensure_ascii=False, indent=2)

print("menu_data.json 생성 완료")
