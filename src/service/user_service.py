from src.model.User import User


def get_user_display_name(user: User, add_user_id: bool = False) -> str:
    """
    Gets the user display name
    :param user: User
    :param add_user_id: Add user id
    :return: User display namE
    """
    return "{}{}{}{}".format(user.tg_first_name,
                             " " + user.tg_last_name if user.tg_last_name is not None else "",
                             " (@" + user.tg_username + ")" if user.tg_username is not None else "",
                             " - " + user.tg_user_id if add_user_id else "")


def get_users_by_string_filter(filter_by: str) -> list[User]:
    """
    Gets users by string filter, searching by first name, last name, username or user id
    :param filter_by: Filter by
    :return: Users
    """

    return User.select().where((User.tg_first_name.contains(filter_by)) |
                               (User.tg_last_name.contains(filter_by)) |
                               (User.tg_username.contains(filter_by)) |
                               (User.tg_user_id.contains(filter_by))
                               ).order_by(User.tg_first_name.desc()).limit(10)
