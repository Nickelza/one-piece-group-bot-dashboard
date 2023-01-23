import streamlit as st

import resources.Environment as Env
from pages.devil_fruits.commons import show_and_get_abilities_multi_select, show_add_form, save
from src.model.DevilFruit import DevilFruit
from src.model.DevilFruitAbility import DevilFruitAbility
from src.model.User import User
from src.model.enums.devil_fruit.DevilFruitAbilityType import DevilFruitAbilityType
from src.model.enums.devil_fruit.DevilFruitStatus import DevilFruitStatus
from src.model.tgrest.TgRestDevilFruitAward import TgRestDevilFruitAward
from src.service.tg_rest_service import send_tg_rest
from src.service.user_service import get_users_by_string_filter, get_user_display_name


def main() -> None:
    """
    View list function
    :return:
    """

    key_suffix = "_list"

    # Filter by status multiselect
    default_status = [DevilFruitStatus.NEW, DevilFruitStatus.COMPLETED, DevilFruitStatus.ENABLED]
    status_filter: list[str] = st.multiselect("Status filter", DevilFruitStatus.get_all_description(),
                                              [status.get_description() for status in default_status])

    selected_statuses = [DevilFruitStatus.get_by_description(status_str) for status_str in status_filter]

    # Filter by name text input
    name_filter = st.text_input("Name filter", "")

    # Get fruits
    devil_fruits: list[DevilFruit] = (DevilFruit.select()
                                      .where((DevilFruit.status.in_(selected_statuses))
                                             & ((DevilFruit.name.contains(name_filter))
                                                | (DevilFruit.model.contains(name_filter))))
                                      .order_by(DevilFruit.id.desc())
                                      .limit(Env.MAX_ITEMS_DISPLAYED_LIST.get_int()))

    for index, devil_fruit in enumerate(devil_fruits):
        key_suffix_list = f"{key_suffix}_{index}"
        status: DevilFruitStatus = DevilFruitStatus(devil_fruit.status)

        with st.expander(devil_fruit.get_full_name()):
            st.info(devil_fruit.get_status_description())
            abilities: list[DevilFruitAbility] = (DevilFruitAbility.select().where(
                DevilFruitAbility.devil_fruit == devil_fruit))

            # Get abilities from multi select
            abilities_type_value_dict: dict[DevilFruitAbilityType, int] = (
                show_and_get_abilities_multi_select(key_suffix_list, existing_abilities=abilities))

            with st.form(f"devil_fruit_edit_form{key_suffix_list}", clear_on_submit=False):
                show_add_form(key_suffix_list, abilities_type_value_dict, devil_fruit=devil_fruit)
                submitted = st.form_submit_button("Save")

                if submitted:
                    save(key_suffix_list, abilities_type_value_dict, devil_fruit=devil_fruit)

            # Award to user section
            # Show if status is completed or enabled
            if status in [DevilFruitStatus.COMPLETED, DevilFruitStatus.ENABLED]:
                st.subheader("Award to user")

                # Filter input box
                filter_user_by = st.text_input(label="Search", key=f"filter_user_by{key_suffix_list}")

                users: list[User] = []
                if len(filter_user_by) > 1:
                    users: list[User] = get_users_by_string_filter(filter_user_by)

                # Map users to display name
                users_display_name_map: list[tuple[str, User]] = [(
                    get_user_display_name(user, add_user_id=True), user) for user in users]

                # Select box with users
                display_name_list = [display_name for display_name, _ in users_display_name_map]
                selected_user_display_name: str = st.selectbox(
                    "Select user", display_name_list, key=f"select_user{key_suffix_list}", index=0,
                    disabled=(len(display_name_list) == 0))

                # Reason input box
                reason: str = st.text_input(label="Reason", key=f"reason{key_suffix_list}")

                # Award button
                if st.button("Award", disabled=(selected_user_display_name is None)):
                    # Get user from display name
                    selected_user: User = next(
                        user for display_name, user in users_display_name_map
                        if display_name == selected_user_display_name)

                    # Reason is required
                    if len(reason) == 0:
                        st.error("Reason is required")
                    else:
                        tg_rest_message = TgRestDevilFruitAward(selected_user.id, devil_fruit.id, reason)
                        send_tg_rest(tg_rest_message)

                        st.success("Devil fruit awarded")
