import streamlit as st
from streamlit_option_menu import option_menu

import constants as c
from pages.users.impel_down import main as impel_down_main
from src.model.User import User


def main():
    """
    Main function
    :return:
    """

    st.title("Users")
    st.markdown(c.HIDE_ST_STYLE, unsafe_allow_html=True)

    key_suffix = "_users"

    # Filter users by first name, last name, username or user id inputted
    filter_by = st.text_input(label="Search", key=f"filter_by{key_suffix}")

    # Filter users limit 10
    if len(filter_by) > 1:
        users: list[User] = User.get_by_string_filter(filter_by)
    else:
        users: list[User] = User.select().order_by(User.last_message_date.desc()).limit(10)

    for index, user in enumerate(users):
        expander_text = user.get_display_name()

        with st.expander(expander_text):
            # Basic information
            col_user_id, col_bounty = st.columns(2)
            col_user_id.text_input("User ID", value=user.tg_user_id, disabled=True,
                                   key=f"user_id_{index}{key_suffix}")
            col_bounty.text_input("Bounty", value=user.get_bounty_formatted(), disabled=True,
                                  key=f"bounty_{index}{key_suffix}")

            # Option Menu
            selected_option_menu = option_menu(
                menu_title=None,
                options=["Impel Down"],
                icons=["shield-lock"],  # https://icons.getbootstrap.com/
                orientation="horizontal",
                key=f"option_menu_{index}{key_suffix}"
            )

            if selected_option_menu == "Impel Down":
                impel_down_main(user)


main()
