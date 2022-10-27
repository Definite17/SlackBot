from slack_bolt.adapter.socket_mode import SocketModeHandler
from utils.slack_client import *
import Tokens
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    handler = SocketModeHandler(get_app(), Tokens.SLACK_APP_TOKEN)
    handler.start()