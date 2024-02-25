from enum import IntEnum

import resources.Environment as Env


class DevilFruitCategory(IntEnum):
    """
    Enum for the category of a devil fruit
    """
    ZOAN = 3
    ANCIENT_ZOAN = 4
    MYTHICAL_ZOAN = 5
    SMILE = 6

    def get_description(self) -> str:
        """
        Get the description of the devil fruit category
        :return: The description of the devil fruit category
        """

        return DEVIL_FRUIT_CATEGORY_DESCRIPTION_MAP[self]

    @staticmethod
    def get_by_description(description: str) -> 'DevilFruitCategory':
        """
        Get the devil fruit category by its description
        :param description: The description of the devil fruit category
        :return: The devil fruit category
        """

        for devil_fruit_category in DevilFruitCategory:
            if devil_fruit_category.get_description() == description:
                return devil_fruit_category

        raise ValueError("Invalid devil fruit category description: " + description)

    @staticmethod
    def get_all_description() -> list[str]:
        """
        Get all the descriptions of the devil fruit categories
        :return: All the descriptions of the devil fruit categories
        """

        # Excluding Logia and Paramecia
        return [DevilFruitCategory.ZOAN.get_description(),
                DevilFruitCategory.ANCIENT_ZOAN.get_description(),
                DevilFruitCategory.MYTHICAL_ZOAN.get_description(),
                DevilFruitCategory.SMILE.get_description()]

    def get_index(self) -> int:
        """
        Get the index of the devil fruit category
        :return: The index of the devil fruit category
        """

        return DEVIL_FRUIT_CATEGORY_INDEX_MAP[self]

    def get_max_sum(self) -> int:
        """
        Get the maximum sum of the devil fruit category
        :return: The sum of the devil fruit category
        """

        return DEVIL_FRUIT_CATEGORY_SUM_MAP[self]


DEVIL_FRUIT_CATEGORY_DESCRIPTION_MAP = {
    DevilFruitCategory.ZOAN: "Zoan",
    DevilFruitCategory.ANCIENT_ZOAN: "Ancient Zoan",
    DevilFruitCategory.MYTHICAL_ZOAN: "Mythical Zoan",
    DevilFruitCategory.SMILE: "SMILE"
}

DEVIL_FRUIT_CATEGORY_INDEX_MAP = {
    DevilFruitCategory.ZOAN: 0,
    DevilFruitCategory.ANCIENT_ZOAN: 1,
    DevilFruitCategory.MYTHICAL_ZOAN: 2,
    DevilFruitCategory.SMILE: 3
}

DEVIL_FRUIT_CATEGORY_SUM_MAP = {
    DevilFruitCategory.ZOAN: Env.DEVIL_FRUIT_CATEGORY_ZOAN_SUM.get_int(),
    DevilFruitCategory.ANCIENT_ZOAN: Env.DEVIL_FRUIT_CATEGORY_ANCIENT_ZOAN_SUM.get_int(),
    DevilFruitCategory.MYTHICAL_ZOAN: Env.DEVIL_FRUIT_CATEGORY_MYTHICAL_ZOAN_SUM.get_int(),
    DevilFruitCategory.SMILE: Env.DEVIL_FRUIT_CATEGORY_ZOAN_SUM.get_int()
}
