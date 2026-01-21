import json
import os

DATA_FILE = "menu_data.json"


def get_menu(day: str, meal: str) -> str | None:
    """
    day: today | tomorrow
    meal: lunch | dinner
    """

    if not os.path.exists(DATA_FILE):
        print("❌ menu_data.json not found")
        return None

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("❌ failed to load menu_data.json:", e)
        return None

    menus = data.get(day, {}).get(meal)
    if not menus:
        print(f"⚠️ no menu for {day} {meal}")
        return None

    day_kr = "오늘" if day == "today" else "내일"
    meal_kr = "점심" if meal == "lunch" else "저녁"

    lines = [f"🍱 {day_kr} {meal_kr} 메뉴", ""]

    for m in menus:
        lines.append(f"[{m.get('course','')}] {m.get('menu','')}")
        for s in m.get("sides", []):
            lines.append(f" - {s}")
        lines.append("")

    return "\n".join(lines).strip()
