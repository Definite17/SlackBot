import os
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
# import zenduty
# from zenduty.api_client import ApiClient

import logging

import Tokens

logging.basicConfig(filename="App.log", level=logging.INFO)

print("Started the BOT")

app = App(
    token=Tokens.SLACK_BOT_TOKEN,
    signing_secret=Tokens.SIGNING_SECRET
)
# app = App(
#     token=os.environ.get('SLACK_BOT_TOKEN'),
#     signing_secret=os.environ.get('SIGNING_SECRET')
# )

# BOT Mention - Demo
@app.event("app_mention")
def event_test(body, say):
    say(f"What's up?")

if __name__ == "__main__":
    SLACK_APP_TOKEN=Tokens.SLACK_APP_TOKEN
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()