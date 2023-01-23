import os
from distutils.util import strtobool

import constants as c


class Environment:
    def __init__(self, name: str, default_value: str = None, can_be_empty: bool = False):
        self.name = name
        self.default_value = default_value
        self.can_be_empty = can_be_empty

    def get_or_none(self) -> str | None:
        """
        Get the environment variable or None if it is not set
        :return: The environment variable or None if it is not set
        :rtype: str | None
        """
        # If default value is set, return the environment variable or the default value
        if self.default_value is not None:
            return os.environ.get(self.name, self.default_value)

        # Get the environment variable or return None if it is not set
        value = os.environ.get(self.name)

        # If the environment variable is not set and the environment variable can be empty, return None
        if value is None and self.can_be_empty:
            return None

        # If the environment variable is not set and the environment variable can not be empty, raise an exception
        if value is None:
            raise Exception(f"Environment variable {self.name} is not set")

        return value

    def get(self) -> str:
        """
        Get the environment variable
        :return: The environment variable
        """
        value = self.get_or_none()
        if value is None:
            raise Exception(f"Environment variable {self.name} is not set")

        return value

    def get_int(self) -> int:
        """
        Get the environment variable as an integer
        :return: The environment variable as an integer
        """
        return int(self.get())

    def get_float(self) -> float:
        """
        Get the environment variable as a float
        :return: The environment variable as a float
        """
        return float(self.get())

    def get_bool(self) -> bool:
        """
        Get the environment variable as a boolean
        :return: The environment variable as a boolean
        """
        return True if strtobool(self.get()) else False

    def get_list(self) -> list[str]:
        """
        Get the environment variable as a list
        :return: The environment variable as a list
        """
        return self.get().split(c.STANDARD_SPLIT_CHAR)


# Bot
OPD_GROUP_BOT_ID = Environment('OPD_GROUP_BOT_ID')
TG_REST_BOT_TOKEN = Environment('TG_REST_BOT_TOKEN')

# TgRest Channel ID
TG_REST_CHANNEL_ID = Environment('TG_REST_CHANNEL_ID')

# CONFIG
# Which timezone to use
TZ = Environment('TZ', default_value='Etc/UTC')

# DATABASE
# Database name
DB_NAME = Environment('DB_NAME')
# Database host
DB_HOST = Environment('DB_HOST')
# Database port
DB_PORT = Environment('DB_PORT')
# Database user
DB_USER = Environment('DB_USER')
# Database password
DB_PASSWORD = Environment('DB_PASSWORD')
# Log queries
DB_LOG_QUERIES = Environment('DB_LOG_QUERIES', default_value='False')

# Should refund wagers default option. Default: False
REFUND_WAGER_DEFAULT = Environment('REFUND_WAGER_DEFAULT', default_value='False')
# Should allow users to bet on multiple choices default option. Default: True
ALLOW_MULTIPLE_CHOICES_DEFAULT = Environment('ALLOW_MULTIPLE_CHOICES_DEFAULT', default_value='True')
# Should allow users to withdraw their bet default option. Default: False
CAN_WITHDRAW_BET_DEFAULT = Environment('CAN_WITHDRAW_BET_DEFAULT', default_value='False')
# Maximum refundable wager for prediction bets. Default: 100 million
PREDICTION_BET_MAX_REFUNDABLE_WAGER = Environment('PREDICTION_BET_MAX_REFUNDABLE_WAGER', default_value='100000000')

# Devil Fruit ability minimum value. Default: 0
DEVIL_FRUIT_ABILITY_MIN_VALUE = Environment('DEVIL_FRUIT_ABILITY_MIN_VALUE', default_value='0')
# Devil Fruit ability maximum value. Default: 100
DEVIL_FRUIT_ABILITY_MAX_VALUE = Environment('DEVIL_FRUIT_ABILITY_MAX_VALUE', default_value='100')
# Devil Fruit abilities maximum sum. Default: 100
DEVIL_FRUIT_ABILITIES_MAX_SUM = Environment('DEVIL_FRUIT_ABILITIES_MAX_SUM', default_value='100')
# Devil Fruit abilities required sum. Default: 100
DEVIL_FRUIT_ABILITIES_REQUIRED_SUM = Environment('DEVIL_FRUIT_ABILITIES_REQUIRED_SUM', default_value='100')

# Maximum items displayed in a list. Default: 10
MAX_ITEMS_DISPLAYED_LIST = Environment('MAX_ITEMS_DISPLAYED_LIST', default_value='10')
