from dotenv import load_dotenv
import os
import json
import traceback
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# ─────────────────────────────
# 1️⃣ Environment Variables
# ─────────────────────────────
load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

print("ENV CHECK")
print("SLACK_BOT_TOKEN:", "OK" if SLACK_BOT_TOKEN else "MISSING")
print("SLACK_APP_TOKEN:", "OK" if SLACK_APP_TOKEN else "MISSING")
print("-" * 60)

if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN:
    raise RuntimeError("error in ENV")

# ─────────────────────────────
# 2️⃣ Slack App
# ─────────────────────────────
app = App(token=SLACK_BOT_TOKEN)

# ─────────────────────────────
# 3️⃣ /menu → Ephemeral Message
# ─────────────────────────────
@app.command("/menu")
def debug_ephemeral_menu(ack, body, client):
    try:
        print("\n/menu COMMAND RECEIVED")
        print(json.dumps(body, indent=2, ensure_ascii=False))

        ack()

        print("ack() called")

        channel_id = body["channel_id"]
        user_id = body["user_id"]

        # Message
        res = client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text="확인하고 싶은 메뉴를 골라주세요.",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "*확인하고 싶은 메뉴를 골라주세요.*\n\n"
                        )
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "오늘 점심"
                            },
                            "value": "today_lunch",
                            "action_id": "today_lunch_click"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "오늘 저녁"
                            },
                            "value": "today_dinner",
                            "action_id": "today_dinner_click"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "내일 점심"
                            },
                            "value": "tomorrow_lunch",
                            "action_id": "tomorrow_lunch_click"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "내일 저녁"
                            },
                            "value": "tomorrow_dinner",
                            "action_id": "tomorrow_dinner_click"
                        }
                    ]
                }
            ]
        )

        print("chat_postEphemeral result:", res.get("ok"))

    except Exception:
        print("ERROR in /menu ephemeral debug")
        print(traceback.format_exc())

# ─────────────────────────────
# 4️⃣ Button Click → Ephemeral Response
# ─────────────────────────────
@app.action("today_lunch_click")
def debug_ephemeral_click(ack, body, client):
    try:
        ack()
        print("\nEPHEMERAL BUTTON CLICKED")
        print(json.dumps(body, indent=2, ensure_ascii=False))

        channel_id = body["channel"]["id"]
        user_id = body["user"]["id"]

        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text="오늘 점심 메뉴입니다!"
        )

        print("Ephemeral response sent for today_lunch_click")

    except Exception:
        print("ERROR in today_lunch_click button handler")
        print(traceback.format_exc())

@app.action("today_dinner_click")
def debug_ephemeral_click(ack, body, client):
    try:
        ack()
        print("\nEPHEMERAL BUTTON CLICKED")
        print(json.dumps(body, indent=2, ensure_ascii=False))

        channel_id = body["channel"]["id"]
        user_id = body["user"]["id"]

        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text="오늘 저녁 메뉴입니다!"
        )

        print("Ephemeral response sent for today_dinner_click")

    except Exception:
        print("ERROR in today_dinner_click button handler")
        print(traceback.format_exc())
        
@app.action("tomorrow_lunch_click")
def debug_ephemeral_click(ack, body, client):
    try:
        ack()
        print("\nEPHEMERAL BUTTON CLICKED")
        print(json.dumps(body, indent=2, ensure_ascii=False))

        channel_id = body["channel"]["id"]
        user_id = body["user"]["id"]

        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text="내일 점심 메뉴입니다!"
        )

        print("Ephemeral response sent for tomorrow_lunch_click")

    except Exception:
        print("ERROR in tomorrow_lunch_click button handler")
        print(traceback.format_exc())

@app.action("tomorrow_dinner_click")
def debug_ephemeral_click(ack, body, client):
    try:
        ack()
        print("\nEPHEMERAL BUTTON CLICKED")
        print(json.dumps(body, indent=2, ensure_ascii=False))

        channel_id = body["channel"]["id"]
        user_id = body["user"]["id"]

        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text="내일 저녁 메뉴입니다!"
        )

        print("Ephemeral response sent for tomorrow_dinner_click")

    except Exception:
        print("ERROR in tomorrow_dinner_click button handler")
        print(traceback.format_exc())

# ─────────────────────────────
# 5️⃣ Run
# ─────────────────────────────
if __name__ == "__main__":
    print("Menu BOT STARTED")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
