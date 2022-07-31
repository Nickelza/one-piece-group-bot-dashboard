from enum import IntEnum


class PredictionStatus(IntEnum):
    NEW = 1
    SENT = 2
    BETS_CLOSED = 3
    RESULT_SET = 4
