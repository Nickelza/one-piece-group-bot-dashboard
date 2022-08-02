from src.model.tgrest.TgRest import TgRest
from src.model.tgrest.TgRestObjectType import TgRestObjectType
from src.model.tgrest.TgRestPredictionAction import TgRestPredictionAction


class TgRestPrediction(TgRest):
    """
    TgRestPrediction class is used to create a Telegram REST API request.
    """

    def __init__(self, action: TgRestPredictionAction, prediction_id: int):
        """
        Constructor
        :param action: The action
        :param prediction_id: The prediction id
        """
        super().__init__(TgRestObjectType.PREDICTION)

        self.action: TgRestPredictionAction = action
        self.prediction_id: int = prediction_id
