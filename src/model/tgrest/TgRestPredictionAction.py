from strenum import StrEnum


class TgRestPredictionAction(StrEnum):
    """
    Enum for the action of Telegram REST API request.
    """
    SEND = 'send'
    REFRESH = 'refresh'
    CLOSE_BETS = 'close_bets'
    SET_RESULTS = 'set_results'
