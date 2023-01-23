from enum import IntEnum


class DevilFruitAbilityType(IntEnum):
    """
    Enum for the type of Devil Fruit ability type.
    """

    DOC_Q_COOLDOWN_DURATION = 1
    FIGHT_COOLDOWN_DURATION = 2
    FIGHT_IMMUNITY_DURATION = 3
    FIGHT_DEFENSE_BOOST = 4
    CHALLENGE_COOLDOWN_DURATION = 5
    PREDICTION_WAGER_REFUND = 6
    GIFT_TAX = 7

    def get_description(self) -> str:
        """
        Get the description of the devil fruit ability type
        :return: The description of the devil fruit ability type
        """
        return DEVIL_FRUIT_ABILITY_TYPE_DESCRIPTION_MAP[self]

    @staticmethod
    def get_all_description():
        """
        Get all the descriptions of the devil fruit ability types
        :return: All the descriptions of the devil fruit ability types
        """
        return [DevilFruitAbilityType.DOC_Q_COOLDOWN_DURATION.get_description(),
                DevilFruitAbilityType.FIGHT_COOLDOWN_DURATION.get_description(),
                DevilFruitAbilityType.FIGHT_IMMUNITY_DURATION.get_description(),
                DevilFruitAbilityType.FIGHT_DEFENSE_BOOST.get_description(),
                DevilFruitAbilityType.CHALLENGE_COOLDOWN_DURATION.get_description(),
                DevilFruitAbilityType.PREDICTION_WAGER_REFUND.get_description(),
                DevilFruitAbilityType.GIFT_TAX.get_description()]

    @staticmethod
    def get_by_description(description: str) -> 'DevilFruitAbilityType':
        """
        Get the devil fruit ability type by its description
        :param description: The description of the devil fruit ability type
        :return: The devil fruit ability type
        """
        for devil_fruit_ability_type in DevilFruitAbilityType:
            if devil_fruit_ability_type.get_description() == description:
                return devil_fruit_ability_type

        raise ValueError("Invalid devil fruit ability type description: " + description)


DEVIL_FRUIT_ABILITY_TYPE_DESCRIPTION_MAP = {
    DevilFruitAbilityType.DOC_Q_COOLDOWN_DURATION: "Doc Q Cooldown Duration",
    DevilFruitAbilityType.FIGHT_COOLDOWN_DURATION: "Fight Cooldown Duration",
    DevilFruitAbilityType.FIGHT_IMMUNITY_DURATION: "Fight Immunity Duration",
    DevilFruitAbilityType.FIGHT_DEFENSE_BOOST: "Fight Defense Boost",
    DevilFruitAbilityType.CHALLENGE_COOLDOWN_DURATION: "Challenge Cooldown Duration",
    DevilFruitAbilityType.PREDICTION_WAGER_REFUND: "Prediction Wager Refund",
    DevilFruitAbilityType.GIFT_TAX: "Gift Tax"
}
