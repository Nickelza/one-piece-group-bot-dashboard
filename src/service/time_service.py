import datetime

import pytz


def convert_seconds_to_time(seconds: int) -> str:
    """
    Converts seconds to days, hours, minutes, seconds
    :param seconds: Seconds to convert
    :return: Days, hours e.g. 1 day 2 hours 5 minutes
    """
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)

    result = ''
    if days > 0:
        if days == 1:
            result += f'{days} day'
        else:
            result += f'{days} days'

    if hours > 0:
        if len(result) > 0:
            result += ' '
        if hours == 1:
            result += f'{hours} hour'
        else:
            result += f'{hours} hours'

    if hours <= 1:  # Show minutes only in last hour
        if len(result) > 0:
            result += ' '
        if minutes > 0:
            if minutes == 1:
                result += f'{minutes} minute'
            else:
                result += f'{minutes} minutes'

    return result


def get_remaining_time(end_datetime: datetime) -> str:
    """
    Get the remaining time until the end_datetime
    :param end_datetime: The end datetime
    :return: The remaining time in days and hours e.g. 1 day 2h hours
    """

    total_seconds = int((pytz.utc.localize(end_datetime) - datetime.datetime.now(pytz.utc)).total_seconds())
    return convert_seconds_to_time(total_seconds)
