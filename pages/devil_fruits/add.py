import streamlit as st

from pages.devil_fruits.commons import show_add_form, show_and_get_abilities_multi_select, save
from src.model.enums.devil_fruit.DevilFruitAbilityType import DevilFruitAbilityType


def main() -> None:
    """
    Add prediction function
    :return:
    """

    key_suffix = "_add"

    # Get abilities from multi select
    abilities_type_value_dict: dict[DevilFruitAbilityType, int] = (
        show_and_get_abilities_multi_select(key_suffix))

    with st.form("devil_fruit_add_form", clear_on_submit=False):
        show_add_form(key_suffix, abilities_type_value_dict)

        submitted = st.form_submit_button("Save")
        if submitted:
            save(key_suffix, abilities_type_value_dict)
