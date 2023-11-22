import streamlit as st

from src.model.exceptions.ValidationException import ValidationException


def get_session_state_key(key: str, suffix: str) -> any:
    """
    Gets the session state key
    :param key: Key
    :param suffix: Suffix
    :return: Session state key
    """

    return st.session_state.get(f"{key}{suffix}")


def validate_not_empty_fields(fields: list[str], key_suffix: str) -> None:
    """
    Validate not empty fields, raise ValidationException if empty
    :param fields: Not empty fields
    :param key_suffix: Key suffix
    :return: None
    """

    for field in fields:
        value = get_session_state_key(field, key_suffix)
        if value is None or (isinstance(value, str) and len(value) == 0):
            raise ValidationException(f"{field} cannot be empty")
