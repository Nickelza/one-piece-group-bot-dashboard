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
BOT_ID = Environment('BOT_ID')

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
