from src.model.tgrest.TgRest import TgRest
from src.model.tgrest.TgRestObjectType import TgRestObjectType


class TgRestDevilFruitAward(TgRest):
    """
    TgRestDevilFruitAward class is used to create a Telegram REST API request.
    """

    def __init__(self, user_id: int, devil_fruit_id: int, reason: str):
        """
        Constructor

        :param user_id: The user id
        :param devil_fruit_id: The devil fruit id
        :param reason: The reason why the devil fruit was awarded
        """

        super().__init__(TgRestObjectType.DEVIL_FRUIT_AWARD)

        self.user_id: int = user_id
        self.devil_fruit_id: int = devil_fruit_id
        self.reason: str = reason
