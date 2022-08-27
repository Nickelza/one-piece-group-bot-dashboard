from src.model.tgrest.TgRest import TgRest
from src.model.tgrest.TgRestObjectType import TgRestObjectType


class TgRestPrivateMessage(TgRest):
    """
    TgRestPrediction class is used to create a Telegram REST API request.
    """

    def __init__(self, tg_user_id: str, message: str):
        """
        Constructor
        :param tg_user_id: The telegram user id to send the message to
        :param message: The message
        """
        super().__init__(TgRestObjectType.PRIVATE_MESSAGE)

        self.tg_user_id: str = tg_user_id
        self.message: str = message
