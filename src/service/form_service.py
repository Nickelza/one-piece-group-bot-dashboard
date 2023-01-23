import streamlit as st


def get_session_state_key(key: str, suffix: str) -> any:
    """
    Gets the session state key
    :param key: Key
    :param suffix: Suffix
    :return: Session state key
    """

    return st.session_state.get(f"{key}{suffix}")
