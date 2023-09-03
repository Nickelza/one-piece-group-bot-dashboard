from src.model.ImpelDownLog import ImpelDownLog
from src.model.User import User
from src.model.exceptions.ValidationException import ValidationException


def get_logs_by_string_filter(filter_by: str) -> list[ImpelDownLog]:
    """
    Gets logs by string filter, searching by first name, last name, username, user id, reason, bounty action,
    sentence type
    :param filter_by: Filter by
    :return: Impel Down Logs
    """

    return ImpelDownLog.select().join(User).where((ImpelDownLog.user.tg_first_name.contains(filter_by)) |
                                                  (ImpelDownLog.user.tg_last_name.contains(filter_by)) |
                                                  (ImpelDownLog.user.tg_username.contains(filter_by)) |
                                                  (ImpelDownLog.user.tg_user_id.contains(filter_by)) |
                                                  (ImpelDownLog.reason.contains(filter_by)) |
                                                  (ImpelDownLog.bounty_action.contains(filter_by)) |
                                                  (ImpelDownLog.sentence_type.contains(filter_by))
                                                  ).order_by(ImpelDownLog.id.desc()).limit(10)


def get_log_display_text(log: ImpelDownLog) -> str:
    """
    Gets the log display text
    :param log: Impel Down Log
    :return: Log display text
    """
    return "{}{}{}{}{} ".format(
        "(Reversed) " if log.is_reversed else "",
        log.user.tg_first_name,
        " " + log.user.tg_last_name if log.user.tg_last_name is not None else "",
        " (@" + log.user.tg_username + ")" if log.user.tg_username is not None else "",
        " - " + log.reason if log.reason is not None else "")


def reverse_bounty_action(log: ImpelDownLog) -> None:
    """
    Reverses the bounty action
    :param log: Impel Down Log
    :return: None
    """

    if log.is_reversed:
        raise ValidationException("Bounty action already reversed")

    user: User = log.user

    # Add lost bounty back
    user.bounty += (log.previous_bounty - log.new_bounty)

    # Update user
    user.save()

    # Update log
    log.is_reversed = True
    log.save()
