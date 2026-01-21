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
            text="Post Ephemeral Message",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            "*Ephemeral Debug Message*\n\n"
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
                                "text": "버튼 테스트"
                            },
                            "value": "ephemeral_test",
                            "action_id": "button_test"
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
@app.action("ephemeral_test_click")
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
            text="Server received your button click!"
        )

        print("ephemeral button response sent")

    except Exception:
        print("ERROR in ephemeral button handler")
        print(traceback.format_exc())

# ─────────────────────────────
# 5️⃣ Run
# ─────────────────────────────
if __name__ == "__main__":
    print("Menu BOT STARTED")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
