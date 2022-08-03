import requests

import resources.Environment as Env
from src.model.tgrest.TgRest import TgRest


class TgBotRequestException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class TgBot:
    def __init__(self):
        self.api_url = f"https://api.telegram.org/bot{Env.TG_REST_BOT_TOKEN.get()}/"
        self.parse_mode = "HTML"

    def send_message(self, tg_rest: TgRest) -> requests.Response:
        """
        Send a message to a Telegram chat
        :param tg_rest: The Telegram REST API request
        :return:
        """
        url = self.api_url + "sendMessage"
        params = {
            "chat_id": Env.TG_REST_CHANNEL_ID.get(),
            "text": "<code>" + tg_rest.get_as_json_string() + "</code>",
            "parse_mode": self.parse_mode
        }
        response = requests.post(url, params)
        if response.status_code != 200:
            raise TgBotRequestException(f"Error: {response.text}")

        return response
