import json

import resources.Environment as Env
from src.model.tgrest.TgRestObjectType import TgRestObjectType


class TgRestException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class TgRest:
    """
    TgRest class is used to create a Telegram REST API request.
    """

    def __init__(self, object_type: TgRestObjectType, **kwargs):
        """
        Constructor
        :param object_type: The object type
        """
        self.bot_id: str = Env.TG_REST_BOT_ID.get()
        self.object_type: TgRestObjectType = object_type

    def get_as_json_string(self) -> str:
        """
        Gets the request as json
        :return: The request as json string
        """

        return json.dumps(self.__dict__)
