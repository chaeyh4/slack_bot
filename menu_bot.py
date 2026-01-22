from dotenv import load_dotenv
import os
import json
import traceback
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from menu_store import get_menu

# ─────────────────────────────
# ENV
# ─────────────────────────────
load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

print("ENV CHECK")
print("SLACK_BOT_TOKEN:", "OK" if SLACK_BOT_TOKEN else "MISSING")
print("SLACK_APP_TOKEN:", "OK" if SLACK_APP_TOKEN else "MISSING")
print("-" * 50)

if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN:
    raise RuntimeError("ENV ERROR")

app = App(token=SLACK_BOT_TOKEN)

# ─────────────────────────────
# /menu command handler
# ─────────────────────────────
@app.command("/menu")
def show_menu_buttons(ack, body, client):
    try:
        print("\n/menu COMMAND RECEIVED")
        print(json.dumps(body, indent=2, ensure_ascii=False))

        ack()

        client.chat_postEphemeral(
            channel=body["channel_id"],
            user=body["user_id"],
            text="메뉴 선택",
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "*확인하고 싶은 메뉴를 골라주세요*"}
                },
                {
                    "type": "actions",
                    "elements": [
                        {"type": "button", "text": {"type": "plain_text", "text": "오늘 점심"}, "action_id": "today_lunch_click"},
                        {"type": "button", "text": {"type": "plain_text", "text": "오늘 저녁"}, "action_id": "today_dinner_click"},
                        {"type": "button", "text": {"type": "plain_text", "text": "내일 점심"}, "action_id": "tomorrow_lunch_click"},
                        {"type": "button", "text": {"type": "plain_text", "text": "내일 저녁"}, "action_id": "tomorrow_dinner_click"},
                    ]
                }
            ]
        )

        print("Menu buttons sent")

    except Exception:
        print("ERROR in /menu")
        print(traceback.format_exc())

# ─────────────────────────────
# button handler + menu_store
# ─────────────────────────────
def send_menu(client, body, day, meal):
    text = get_menu(day, meal)
    if not text:
        text = "😢 메뉴 정보가 없습니다."

    client.chat_postEphemeral(
        channel=body["channel"]["id"],
        user=body["user"]["id"],
        text=text
    )

@app.action("today_lunch_click")
def today_lunch(ack, body, client):
    ack()
    print("TODAY LUNCH CLICKED")
    send_menu(client, body, "today", "lunch")

@app.action("today_dinner_click")
def today_dinner(ack, body, client):
    ack()
    print("TODAY DINNER CLICKED")
    send_menu(client, body, "today", "dinner")

@app.action("tomorrow_lunch_click")
def tomorrow_lunch(ack, body, client):
    ack()
    print("TOMORROW LUNCH CLICKED")
    send_menu(client, body, "tomorrow", "lunch")

@app.action("tomorrow_dinner_click")
def tomorrow_dinner(ack, body, client):
    ack()
    print("TOMORROW DINNER CLICKED")
    send_menu(client, body, "tomorrow", "dinner")

# ─────────────────────────────
# Run
# ─────────────────────────────
if __name__ == "__main__":
    print("\nMENU BOT STABLE + STORE STARTED")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
