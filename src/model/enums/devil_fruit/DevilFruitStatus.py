from enum import IntEnum


class DevilFruitStatus(IntEnum):
    """
    Enum for the status of a Devil Fruit
    """

    NEW = 1  # Just created
    COMPLETED = 2  # Abilities added
    ENABLED = 3  # Enabled in the system
    ENQUEUED = 4  # Enqueued for sending
    RELEASED = 5  # Released in the system
    COLLECTED = 6  # Collected by a user
    EATEN = 7  # Eaten by a user

    def get_description(self) -> str:
        """
        Get the description of the devil fruit status
        :return: The description of the devil fruit status
        """

        return DEVIL_FRUIT_STATUS_DESCRIPTION_MAP[self]

    @staticmethod
    def get_by_description(description: str) -> 'DevilFruitStatus':
        """
        Get the devil fruit status by its description
        :param description: The description of the devil fruit status
        :return: The devil fruit status
        """

        for devil_fruit_status in DevilFruitStatus:
            if devil_fruit_status.get_description() == description:
                return devil_fruit_status

        raise ValueError("Invalid devil fruit status description: " + description)

    @staticmethod
    def get_all_description() -> list[str]:
        """
        Get all the descriptions of the devil fruit statuses
        :return: All the descriptions of the devil fruit statuses
        """

        return [DevilFruitStatus.NEW.get_description(),
                DevilFruitStatus.COMPLETED.get_description(),
                DevilFruitStatus.ENABLED.get_description(),
                DevilFruitStatus.ENQUEUED.get_description(),
                DevilFruitStatus.RELEASED.get_description(),
                DevilFruitStatus.COLLECTED.get_description(),
                DevilFruitStatus.EATEN.get_description()]

    def is_enabled(self) -> bool:
        """
        Check if the devil fruit is enabled
        :return: True if the devil fruit is enabled
        """

        return self not in [DevilFruitStatus.NEW, DevilFruitStatus.COMPLETED]

    @staticmethod
    def get_is_completed_list() -> list['DevilFruitStatus']:
        """
        Get a list of all completed statuses
        :return: List of completed statuses
        """

        return [DevilFruitStatus.COMPLETED, DevilFruitStatus.ENABLED, DevilFruitStatus.ENQUEUED,
                DevilFruitStatus.RELEASED, DevilFruitStatus.COLLECTED, DevilFruitStatus.EATEN]


DEVIL_FRUIT_STATUS_DESCRIPTION_MAP = {
    DevilFruitStatus.NEW: "New",
    DevilFruitStatus.COMPLETED: "Completed",
    DevilFruitStatus.ENABLED: "Enabled",
    DevilFruitStatus.ENQUEUED: "Enqueued",
    DevilFruitStatus.RELEASED: "Released",
    DevilFruitStatus.COLLECTED: "Collected",
    DevilFruitStatus.EATEN: "Eaten"
}
