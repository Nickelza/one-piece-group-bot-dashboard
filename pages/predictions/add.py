import streamlit as st

from pages.predictions.commons import get_add_form_optionals, get_add_form, save


def main() -> None:
    """
    Add prediction function
    :return:
    """

    key_suffix = "_add"

    # Get form optionals
    options_count, should_send, should_end, default_time_value = get_add_form_optionals(key_suffix)

    with st.form("prediction_add_form", clear_on_submit=False):
        get_add_form(options_count, should_send, should_end, default_time_value, key_suffix)

        submitted = st.form_submit_button("Save Poll")
        if submitted:
            save(should_send, should_end, options_count, key_suffix)

