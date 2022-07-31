from enum import Enum


class PredictionType(Enum):
    """
    Enum class for predictions type
    """
    VERSUS = "Versus"
    PREFERENCE = "Preference"
    EVENT = "Event"
