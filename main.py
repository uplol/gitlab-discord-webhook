import os

from flask import Flask, request, abort

from webhook import webhook_push, send_webhook

# Load some config
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", default=None)
if not DISCORD_WEBHOOK_URL:
    raise ValueError("You must define a DISCORD_WEBHOOK_URL env var!")

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", default=None)
if not WEBHOOK_SECRET:
    raise ValueError("You must define a WEBHOOK_SECRET env var!")

# Initialize flask app
app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    secret = request.args.get("secret")
    if not secret or secret != WEBHOOK_SECRET:
        return abort(403, "Unauthorized! Invalid secret!")

    event_type = request.headers.get("X-Gitlab-Event")
    embed = None
    if event_type == "Push Hook":
        data = request.get_json()
        embed = webhook_push()

    if embed:
        send_webhook(embed, DISCORD_WEBHOOK_URL).raise_for_status()
        return "Ok"


if __name__ == "__main__":
    app.run()
