import requests

import resources.Environment as Env
from src.model.tgrest.TgBotRequestException import TgBotRequestException
from src.model.tgrest.TgRest import TgRest


class TgBot:
    def __init__(self):
        self.api_url = f"https://api.telegram.org/bot{Env.TG_REST_BOT_TOKEN.get()}/"
        self.parse_mode = "HTML"

    def send_message(self, tg_rest: TgRest):
        url = self.api_url + "sendMessage"
        params = {
            "chat_id": Env.TG_REST_CHANNEL_ID.get(),
            "text": "<code>" + tg_rest.get_as_json_string() + "</code>",
            "parse_mode": self.parse_mode
        }
        response = requests.post(url, params)
        if response.status_code != 200:
            raise TgBotRequestException(f"Error: {response.text}")
