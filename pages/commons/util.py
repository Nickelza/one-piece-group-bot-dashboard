import streamlit as st

from src.model.User import User


def select_user_select_box(key_suffix: str) -> tuple[str, list[tuple[str, User]]]:
    """
    Select user select box
    :param key_suffix: The key suffix for the select box
    :return: Selected user display name, users display name map
    """

    # Filter input box
    filter_user_by = st.text_input(label="Search users", key=f"filter_user_by{key_suffix}")

    users: list[User] = []
    if len(filter_user_by) > 1:
        users: list[User] = User.get_by_string_filter(filter_user_by)

    # Map users to display name
    users_display_name_map: list[tuple[str, User]] = [(
        user.get_display_name(add_user_id=True), user) for user in users]

    # Select box with users
    display_name_list = [display_name for display_name, _ in users_display_name_map]
    selected_user_display_name: str = st.selectbox(
        "Select user", display_name_list, key=f"select_user{key_suffix}", index=0,
        disabled=(len(display_name_list) == 0))
    return selected_user_display_name, users_display_name_map


def get_selected_user(display_name: str, users_display_name_map: list[tuple[str, User]]) -> User:
    """
    Gets the selected user
    :param display_name: Display name
    :param users_display_name_map: Users display name map
    :return: Selected user
    """

    # Get user from display name
    for user_display_name, user in users_display_name_map:
        if user_display_name == display_name:
            return user
