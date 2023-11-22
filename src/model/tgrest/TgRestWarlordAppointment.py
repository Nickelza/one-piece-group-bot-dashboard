from src.model.tgrest.TgRest import TgRest
from src.model.tgrest.TgRestObjectType import TgRestObjectType


class TgRestWarlordAppointment(TgRest):
    """
    TgRestWarlordAppointment class is used to create a Telegram REST API request.
    """

    def __init__(self, user_id: int, warlord_id: int, days: int):
        """
        Constructor

        :param user_id: The user id
        :param warlord_id: The warlord id
        :param days: The number of days the user will be a warlord. Technically not necessary since it can be calculated
                     from the end date, but it's easier to just pass it in.
        """

        super().__init__(TgRestObjectType.WARLORD_APPOINTMENT)

        self.user_id: int = user_id
        self.warlord_id: int = warlord_id
        self.days: int = days
