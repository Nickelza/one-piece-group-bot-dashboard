from datetime import datetime

import streamlit as st

from pages.warlords.commons import show_add_form, save
from src.model.User import User
from src.model.Warlord import Warlord
from src.model.tgrest.TgRestWarlordRevocation import TgRestWarlordRevocation
from src.service.tg_rest_service import send_tg_rest


def main() -> None:
    """
    View list function
    :return:
    """

    key_suffix = "_list"

    # Only active checkbox
    only_active = st.checkbox("Only active", value=True)

    # Filter records by first name, last name, username, user id, epithet, reason
    filter_by = st.text_input(
        label="Search", key=f"filter_by{key_suffix}",
        help="Search by first name, last name, username, user id, epithet, reason")

    # Get warlords
    if len(filter_by) > 1:
        warlords: list[Warlord] = Warlord.get_by_string_filter(filter_by, only_active=only_active)
    else:
        warlords: list[Warlord] = Warlord.get_all(only_active=only_active)

    for index, warlord in enumerate(warlords):
        key_suffix_list = f"{key_suffix}_{index}"

        user: User = warlord.user
        with st.expander(user.get_display_name()):

            if not only_active:
                if warlord.is_active():
                    st.info("Active")
                else:
                    st.error("Inactive")

            # Start and end date
            col_start_date, col_end_date = st.columns(2)
            col_start_date.text_input("Start date", value=warlord.date, disabled=True,
                                      key=f"start_date{key_suffix_list}")
            col_end_date.text_input("End date", value=warlord.end_date, disabled=True,
                                    key=f"end_date{key_suffix_list}")

            with st.form(f"warlord_edit_form{key_suffix_list}", clear_on_submit=False):
                show_add_form(key_suffix_list, warlord=warlord)
                submitted = st.form_submit_button("Save")

                if submitted:
                    save(key_suffix_list, user, warlord)

            # Show if is active
            if warlord.is_active():
                # Revoke membership section
                st.subheader("Revoke membership")

                # Reason input box
                reason: str = st.text_input(label="Reason", key=f"revoke_reason_{key_suffix_list}")
                # Revoke button
                if st.button("Revoke membership", key=f"revoke{key_suffix_list}"):

                    # Reason is required
                    if len(reason) == 0:
                        st.error("Reason is required")
                    else:
                        warlord.end_date = datetime.now()
                        warlord.revoke_reason = reason
                        warlord.save()

                        st.success("Warlord membership revoked, refresh the page")

                        tg_rest_message = TgRestWarlordRevocation(user.id, warlord.id)
                        send_tg_rest(tg_rest_message)
