from src.model.tgrest.TgRest import TgRest
from src.model.tgrest.TgRestObjectType import TgRestObjectType


class TgRestWarlordRevocation(TgRest):
    """
    TgRestWarlordRevocation class is used to create a Telegram REST API request.
    """

    def __init__(self, user_id: int, warlord_id: int):
        """
        Constructor

        :param user_id: The user id
        :param warlord_id: The warlord id
        """

        super().__init__(TgRestObjectType.WARLORD_REVOCATION)

        self.user_id: int = user_id
        self.warlord_id: int = warlord_id
