import datetime


def get_remaining_time_in_seconds(end_datetime: datetime, start_datetime: datetime = None) -> int:
    """
    Get the remaining time in seconds until the end_datetime
    :param end_datetime: The end datetime
    :param start_datetime: The start datetime. If None, the current datetime is used
    :return: The remaining time in seconds
    """
    # Remove offset awareness from end_datetime
    end_datetime = end_datetime.replace(tzinfo=None)
    if start_datetime is None:
        start_datetime = datetime.datetime.now(datetime.timezone.utc)
    start_datetime = start_datetime.replace(tzinfo=None)

    # If the end_datetime is in the past, return 0
    if end_datetime < start_datetime:
        return 0

    return int((end_datetime - start_datetime).total_seconds())


def get_remaining_time_in_days(end_datetime: datetime, start_datetime: datetime = None) -> int:
    """
    Get the remaining time in days until the end_datetime
    :param end_datetime: The end datetime
    :param start_datetime: The start datetime. If None, the current datetime is used
    :return: The remaining time in days
    """
    return int(get_remaining_time_in_seconds(end_datetime, start_datetime) / 86400)


def get_datetime_in_future_seconds(seconds: int, start_time: datetime.datetime = None) -> datetime:
    """
    Get the datetime in the future
    :param seconds: The number of seconds in the future
    :param start_time: The start time. If None, the current datetime is used
    :return: The datetime in the future
    """

    if start_time is None:
        start_time = datetime.datetime.now()

    return start_time + datetime.timedelta(seconds=int(seconds))


def get_datetime_in_future_hours(hours: float) -> datetime:
    """
    Get the datetime in the future
    :param hours: The number of hours in the future
    :return: The datetime in the future
    """

    return get_datetime_in_future_seconds(int(hours * 3600))


def get_datetime_in_future_days(days: int) -> datetime:
    """
    Get the datetime in the future
    :param days: The number of days in the future
    :return: The datetime in the future
    """

    return get_datetime_in_future_hours(days * 24)
