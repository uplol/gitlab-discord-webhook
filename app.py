import os

from flask import Flask, request, abort

from webhook import webhook_push, webhook_pipeline, send_webhook

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
        embed = webhook_push(data)
    if event_type == "Pipeline Hook":
        data = request.get_json()
        if data["object_attributes"]["status"] in ["success", "failed", "manual"]:
            embed = webhook_pipeline(data)

    if embed:
        send_webhook(embed, DISCORD_WEBHOOK_URL)
        return "Ok"

    return abort(400, "Could not create message for event type {}".format(event_type))


if __name__ == "__main__":
    app.run(host="0.0.0.0")

