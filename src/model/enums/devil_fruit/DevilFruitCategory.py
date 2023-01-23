from enum import IntEnum


class DevilFruitCategory(IntEnum):
    """
    Enum for the category of a devil fruit
    """
    LOGIA = 1
    PARAMECIA = 2
    ZOAN = 3

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

        return [DevilFruitCategory.LOGIA.get_description(),
                DevilFruitCategory.PARAMECIA.get_description(),
                DevilFruitCategory.ZOAN.get_description()]

    def get_index(self) -> int:
        """
        Get the index of the devil fruit category
        :return: The index of the devil fruit category
        """

        return DEVIL_FRUIT_CATEGORY_INDEX_MAP[self]


DEVIL_FRUIT_CATEGORY_DESCRIPTION_MAP = {
    DevilFruitCategory.LOGIA: "Logia",
    DevilFruitCategory.PARAMECIA: "Paramecia",
    DevilFruitCategory.ZOAN: "Zoan"
}

DEVIL_FRUIT_CATEGORY_INDEX_MAP = {
    DevilFruitCategory.LOGIA: 0,
    DevilFruitCategory.PARAMECIA: 1,
    DevilFruitCategory.ZOAN: 2
}
