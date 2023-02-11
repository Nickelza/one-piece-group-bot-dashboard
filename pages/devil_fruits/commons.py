import streamlit as st

import resources.Environment as Env
from src.model.DevilFruit import DevilFruit
from src.model.DevilFruitAbility import DevilFruitAbility
from src.model.enums.devil_fruit.DevilFruitAbilityType import DevilFruitAbilityType
from src.model.enums.devil_fruit.DevilFruitCategory import DevilFruitCategory
from src.model.enums.devil_fruit.DevilFruitStatus import DevilFruitStatus
from src.model.exceptions.ValidationException import ValidationException
from src.service.form_service import get_session_state_key


def show_add_form(key_suffix: str, abilities_type_value_dict: dict[DevilFruitAbilityType, int],
                  devil_fruit: DevilFruit = None) -> None:
    """
    Show add form
    :param key_suffix: Key suffix
    :param abilities_type_value_dict: The abilities type and their values
    :param devil_fruit: The devil fruit
    :return: None
    """

    # Can't be edited once scheduled for release
    _is_editable: bool = is_editable(devil_fruit)

    # Category
    category_index = (DevilFruitCategory(devil_fruit.category).get_index() if devil_fruit is not None else 0)
    st.selectbox("Category", DevilFruitCategory.get_all_description(), key=f"category{key_suffix}",
                 index=category_index, disabled=_is_editable)

    # Name
    name_value = devil_fruit.name if devil_fruit is not None else ""
    st.text_input("Name", name_value, key=f"name{key_suffix}", disabled=_is_editable)

    # Model - Only for Zoans
    model_value = devil_fruit.model if devil_fruit is not None else ""
    st.text_input("Model", model_value, key=f"model{key_suffix}", disabled=_is_editable)

    # Abilities - List of number inputs
    ability_min_value: int = Env.DEVIL_FRUIT_ABILITY_MIN_VALUE.get_int()
    ability_max_value: int = Env.DEVIL_FRUIT_ABILITY_MAX_VALUE.get_int()
    for ability_type, ability_value in abilities_type_value_dict.items():
        st.number_input(ability_type.get_description(), key=get_ability_input_key(key_suffix, ability_type),
                        min_value=ability_min_value, max_value=ability_max_value, disabled=_is_editable,
                        value=ability_value)

    # Enabled checkbox - Only if list of abilities is not empty (else disabled)
    is_enabled = devil_fruit is not None and DevilFruitStatus(devil_fruit.status).is_enabled()
    can_change_is_enabled = True

    if len(abilities_type_value_dict) == 0:
        is_enabled = can_change_is_enabled = False

    if _is_editable:
        can_change_is_enabled = False

    st.checkbox("Enabled", key=f"enabled{key_suffix}", value=is_enabled, disabled=(not can_change_is_enabled))


def show_and_get_abilities_multi_select(key_suffix: str, existing_abilities: list[DevilFruitAbility] = None
                                        ) -> dict[DevilFruitAbilityType, int]:
    """
    Show and get abilities multi select
    :param key_suffix: Key suffix
    :param existing_abilities: The existing abilities (if any)
    :return: The abilities and their values
    """

    abilities_description: list[str] = []
    if existing_abilities is not None:
        abilities_description: list[str] = [DevilFruitAbilityType(ability.ability_type).get_description()
                                            for ability in existing_abilities]

    # Multi select with all abilities
    selected_abilities_description: list[str] = st.multiselect(
        "Abilities", options=DevilFruitAbilityType.get_all_description(), default=abilities_description,
        key=f"abilities{key_suffix}", disabled=is_editable(abilities=existing_abilities))

    abilities_type_value_dict: dict[DevilFruitAbilityType, int] = {}
    for ability_description in selected_abilities_description:
        ability_type: DevilFruitAbilityType = DevilFruitAbilityType.get_by_description(ability_description)
        ability_value: int = 0

        if existing_abilities is not None:
            for ability in existing_abilities:
                if DevilFruitAbilityType(ability.ability_type) is ability_type:
                    ability_value = int(ability.value)

        abilities_type_value_dict[ability_type] = ability_value

    return abilities_type_value_dict


def validate(key_suffix: str, abilities_type_value_dict: dict[DevilFruitAbilityType, int],
             ) -> tuple[DevilFruitCategory, str, str, bool, bool]:
    """
    Validate the devil fruit, raise exception if not valid
    :param key_suffix: Key suffix
    :param abilities_type_value_dict: The abilities type and their values
    :return: tuple with the category, name, model, is completed and is enabled
    """

    # Name should be 1 word "es. Gomu" or 4 words "es. Gomu Gomu no Mi"
    name_components: list[str] = str(get_session_state_key("name", key_suffix)).strip().split(" ")

    if len(name_components) not in [1, 4]:
        raise ValidationException("Name should be 1 word (ex. Gomu) or 4 words (ex. Gomu Gomu no Mi)")
    name = compose_name(name_components)

    # Model required for Zoan, not allowed for others
    category: DevilFruitCategory = DevilFruitCategory.get_by_description(get_session_state_key("category", key_suffix))
    model = str(get_session_state_key("model", key_suffix).strip()).capitalize()
    if category in [DevilFruitCategory.ZOAN, DevilFruitCategory.ANCIENT_ZOAN, DevilFruitCategory.MYTHICAL_ZOAN]:
        if model == "":
            raise ValidationException("Model required for Zoan type Devil Fruit")
    elif model != "":
        raise ValidationException("Model not allowed for this category of Devil Fruit")

    if model == "":
        model = None

    # Already existing devil fruit with same name and model
    existing_devil_fruit: DevilFruit = DevilFruit.get_or_none(name=name, model=model)
    if existing_devil_fruit is not None and existing_devil_fruit != existing_devil_fruit:
        raise ValidationException(
            f"Devil Fruit already exists with same name already exists: {existing_devil_fruit.get_full_name()}")

    # Validate ability not 0 and the sum of abilities not greater than max
    sum_abilities: int = 0
    for ability_type, ability_value in abilities_type_value_dict.items():
        ability_value = get_session_state_key(f'ability{ability_type}', key_suffix)
        if ability_value == 0:
            raise ValidationException(f"Ability {ability_type.get_description()} can't be 0")

        sum_abilities += get_session_state_key(f'ability{ability_type}', key_suffix)
        if sum_abilities > category.get_max_sum():
            raise ValidationException(
                f"Sum of abilities cannot be greater than {category.get_max_sum()}")

    # Sum of abilities of required value, consider complete and enable status
    is_completed = False
    is_enabled = get_session_state_key("enabled", key_suffix)

    if sum_abilities == category.get_max_sum():
        is_completed = True
    elif is_enabled:
        # Trying to enable before completing - Error
        raise ValidationException(f"Sum of abilities should be {category.get_max_sum()}"
                                  f" before enabling")

    if is_enabled and category is DevilFruitCategory.MYTHICAL_ZOAN:  # Mythical Zoan can't be enabled, only awarded
        raise ValidationException(
            f"Devil Fruit of category {category.get_description()} can't be enabled for scheduling")

    # Completed, check if already exists a fruit with same abilities
    if len(abilities_type_value_dict) > 0:
        duplicate_devil_fruit: DevilFruit = get_duplicate_fruit(abilities_type_value_dict)
        if duplicate_devil_fruit is not None and duplicate_devil_fruit != existing_devil_fruit:
            raise ValidationException(
                f"Devil Fruit already exists with same abilities: {duplicate_devil_fruit.get_full_name()}")

    return category, name, model, is_completed, is_enabled


def compose_name(name_components: list[str]) -> str:
    """
    Compose the name
    :param name_components: The name components
    :return: The composed name
    """

    # If 1 word, replicate it and add "no Mi"
    if len(name_components) == 1:
        name_components.append(name_components[0])
        name_components.append("no Mi")

    # Capitalize first letter of each word
    new_name = " ".join(name_components).title()

    # Replace "No Mi" with "no Mi"
    new_name = new_name.replace("No Mi", "no Mi")

    return new_name


def get_ability_input_key(key_suffix: str, ability_type: DevilFruitAbilityType) -> str:
    """
    Get the ability input key
    :param key_suffix: Key suffix
    :param ability_type: The ability type
    :return: The ability input key
    """

    return f"ability{ability_type}{key_suffix}"


def save(key_suffix: str, abilities_type_value_dict: dict[DevilFruitAbilityType, int],
         devil_fruit: DevilFruit = None) -> None:
    """
    Save the devil fruit
    :param key_suffix: Key suffix
    :param abilities_type_value_dict: The abilities type value dict list
    :param devil_fruit: Already existing devil fruit
    :return: None
    """

    is_new = devil_fruit is None
    if is_new:
        devil_fruit = DevilFruit()

    try:
        category, name, model, is_completed, is_enabled = validate(key_suffix, abilities_type_value_dict)
        try:
            devil_fruit.category = category
            devil_fruit.name = name
            devil_fruit.model = model

            devil_fruit.status = DevilFruitStatus.NEW
            if is_completed:
                devil_fruit.status = DevilFruitStatus.COMPLETED
            if is_enabled:
                devil_fruit.status = DevilFruitStatus.ENABLED

            # Save the devil fruit
            devil_fruit.save()

            # Delete the previous abilities
            if not is_new:
                DevilFruitAbility.delete().where(DevilFruitAbility.devil_fruit == devil_fruit).execute()

            # Save the new abilities
            for ability_type, ability_value in abilities_type_value_dict.items():
                ability_value = get_session_state_key(f'ability{ability_type}', key_suffix)

                # On single lines to enable IDE detection of the type
                devil_fruit_ability = DevilFruitAbility()
                devil_fruit_ability.devil_fruit = devil_fruit
                devil_fruit_ability.ability_type = ability_type
                devil_fruit_ability.value = ability_value
                devil_fruit_ability.save()

            st.success("Devil Fruit saved" if is_new else "Devil Fruit updated")
        except Exception as e:
            st.error(f"Error saving the devil fruit: {e}")
    except ValidationException as ve:
        st.error(ve)


def get_duplicate_fruit(abilities_type_value_dict: dict[DevilFruitAbilityType, int]) -> DevilFruit | None:
    """
    Get the duplicate fruit
    :param abilities_type_value_dict: The abilities type value dict list
    :return: The duplicate fruit or None
    """

    # Get all completed devil fruits
    devil_fruits: list[DevilFruit] = (DevilFruit.select()
                                      .where(DevilFruit.status.in_(DevilFruitStatus.get_is_completed_list())))

    # Check if any of the devil fruits has the same abilities
    for devil_fruit in devil_fruits:
        devil_fruit_abilities: list[DevilFruitAbility] = (DevilFruitAbility.select()
                                                          .where(DevilFruitAbility.devil_fruit == devil_fruit))
        existing_devil_fruit_abilities_dict: dict[DevilFruitAbilityType, int] = {}
        for devil_fruit_ability in devil_fruit_abilities:
            existing_devil_fruit_abilities_dict[DevilFruitAbilityType(devil_fruit_ability.ability_type)] = (
                devil_fruit_ability.value)

        if existing_devil_fruit_abilities_dict == abilities_type_value_dict:
            return devil_fruit

    return None


def is_editable(devil_fruit: DevilFruit = None, abilities: list[DevilFruitAbility] = None) -> bool:
    """
    Check if the devil fruit can be edited, false if it's already enqueued
    :param devil_fruit: The devil fruit
    :param abilities: The abilities
    :return: True if it can be edited, False otherwise
    """

    if abilities is not None and len(abilities) > 0:
        devil_fruit: DevilFruit = abilities[0].devil_fruit

    return devil_fruit is not None and DevilFruitStatus(devil_fruit.status) in [
        DevilFruitStatus.SCHEDULED, DevilFruitStatus.RELEASED, DevilFruitStatus.COLLECTED, DevilFruitStatus.EATEN]
