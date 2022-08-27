import re

import streamlit as st

from src.model.User import User
from src.model.tgrest.TgBot import TgBot
from src.model.tgrest.TgBot import TgBotRequestException
from src.model.tgrest.TgRest import TgRest
from src.model.tgrest.TgRestPrivateMessage import TgRestPrivateMessage


def send_tg_rest_message(user: User, message: str, success_message: str = None) -> None:
    """
    Send tg rest command
    :param user: User
    :param message: Message to send
    :param success_message: Success message
    :return:
    """

    # Send command
    tg_rest_private_message = TgRestPrivateMessage(user.tg_user_id, message)
    return send_tg_rest(tg_rest_private_message, success_message)


def send_tg_rest(tg_rest: TgRest, success_message: str = None) -> None:
    """
    Send tg rest command
    :param tg_rest: TgRest
    :param success_message: Success message
    :return:
    """

    # Send command
    try:
        TgBot().send_message(tg_rest)

        if success_message is not None:
            st.success(success_message)
    except TgBotRequestException as e:
        st.error(e.message)
        return


def escape_valid_markdown_chars(text: str) -> str:
    """
    Escape valid markdown chars
    :param text: Text
    :return: Escaped text
    """

    escape_chars = r'_*[]()'

    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)
