import streamlit as st

import resources.Environment as Env
from pages.devil_fruits.commons import show_and_get_abilities_multi_select, show_add_form, save
from src.model.DevilFruit import DevilFruit
from src.model.DevilFruitAbility import DevilFruitAbility
from src.model.enums.devil_fruit.DevilFruitAbilityType import DevilFruitAbilityType
from src.model.enums.devil_fruit.DevilFruitStatus import DevilFruitStatus


def main() -> None:
    """
    View list function
    :return:
    """

    key_suffix = "_list"

    # Filter by status multiselect
    default_status = [DevilFruitStatus.NEW, DevilFruitStatus.COMPLETED, DevilFruitStatus.ENABLED]
    status_filter = st.multiselect("Status filter", DevilFruitStatus.get_all_description(),
                                   [status.get_description() for status in default_status])

    selected_statuses = [DevilFruitStatus.get_by_description(status) for status in status_filter]

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

        with st.expander(devil_fruit.get_full_name()):
            st.info(devil_fruit.get_status_description())
            abilities: list[DevilFruitAbility] = (DevilFruitAbility.select().where(
                DevilFruitAbility.devil_fruit == devil_fruit))

            # Get abilities from multi select
            abilities_type_value_dict_list: list[dict[DevilFruitAbilityType, int]] = (
                show_and_get_abilities_multi_select(key_suffix_list, abilities=abilities))

            with st.form(f"devil_fruit_edit_form{key_suffix_list}", clear_on_submit=False):
                show_add_form(key_suffix_list, abilities_type_value_dict_list, devil_fruit=devil_fruit)
                submitted = st.form_submit_button("Save")

                if submitted:
                    save(key_suffix_list, abilities_type_value_dict_list, devil_fruit=devil_fruit)
