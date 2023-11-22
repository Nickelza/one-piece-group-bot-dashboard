from datetime import datetime

import streamlit as st

import resources.Environment as Env
from src.model.User import User
from src.model.Warlord import Warlord
from src.model.exceptions.ValidationException import ValidationException
from src.model.tgrest.TgRestWarlordAppointment import TgRestWarlordAppointment
from src.service.date_service import get_remaining_time_in_days, get_datetime_in_future_days
from src.service.form_service import get_session_state_key, validate_not_empty_fields
from src.service.tg_rest_service import send_tg_rest


def show_add_form(key_suffix: str, warlord: Warlord = None) -> None:
    """
    Show add form
    :param key_suffix: Key suffix
    :param warlord: The warlord
    :return: None
    """

    is_disabled = False
    if warlord and not warlord.is_active():
        is_disabled = True

    # Epithet
    epithet_value = warlord.epithet if warlord else ""
    st.text_input(label="Epithet", value=epithet_value, key=f"epithet{key_suffix}", max_chars=99,
                  disabled=is_disabled)

    # Reason
    reason_value = warlord.reason if warlord else ""
    st.text_input(label="Reason", value=reason_value, key=f"reason{key_suffix}", max_chars=999, disabled=is_disabled)

    # Duration
    # Min value can be 0 if a warlord was appointed and revoked in less than a day
    duration_value = get_remaining_time_in_days(warlord.end_date, warlord.date) if warlord else 7
    st.number_input(label="Duration in days", value=duration_value, key=f"duration{key_suffix}",
                    min_value=(0 if warlord else 0), max_value=365, disabled=is_disabled)


def validate(key_suffix: str, user: User, warlord: Warlord) -> None:
    """
    Validate the warlord, raise exception if not valid
    :param key_suffix: Key suffix
    :param user: The user
    :param warlord: The warlord
    :return: None
    """

    validate_not_empty_fields(["epithet", "reason", "duration"], key_suffix)

    is_new = warlord is None

    # New appointment
    if is_new:
        # User is already a warlord
        if user.is_warlord():
            raise ValidationException(f"User {user.get_display_name()} is already a warlord")

        # Max number of warlords reached
        if Warlord.get_active_count() >= Env.MAX_WARLORDS.get_int():
            raise ValidationException(f"Max number of warlords reached: {Env.MAX_WARLORDS.get_int()}")
    else:
        # No longer a warlord
        if warlord.end_date < datetime.now():
            raise ValidationException(f"Expired warlord cannot be updated")

        # Duration less than already elapsed days
        duration = get_session_state_key("duration", key_suffix)
        if datetime.now() > warlord.get_end_date_by_duration(duration):
            elapsed_days = get_remaining_time_in_days(warlord.end_date, warlord.date)
            raise ValidationException(f"Duration cannot be less than already elapsed days: {elapsed_days}")

    epithet: str = get_session_state_key("epithet", key_suffix)

    # Active warlord with same epithet that is not the user already existing
    existing_warlord_with_epithet: Warlord = Warlord.get_or_none((Warlord.end_date > datetime.now())
                                                                 & (Warlord.user != user)
                                                                 & (Warlord.epithet == epithet))
    if existing_warlord_with_epithet:
        raise ValidationException(f"Warlord with epithet {epithet} already exists")


def save(key_suffix: str, user: User, warlord: Warlord | None) -> None:
    """
    Save the devil fruit
    :param key_suffix: Key suffix
    :param user: The user
    :param warlord: The warlord
    :return: None
    """

    is_new = warlord is None

    try:
        validate(key_suffix, user, warlord)
        try:
            duration = get_session_state_key("duration", key_suffix)
            if is_new:
                end_date = get_datetime_in_future_days(duration)
                warlord = Warlord()
                warlord.user = user
                warlord.original_end_date = end_date
            else:
                end_date = warlord.get_end_date_by_duration(duration)

            warlord.epithet = get_session_state_key("epithet", key_suffix)
            warlord.reason = get_session_state_key("reason", key_suffix)
            warlord.end_date = end_date
            warlord.save()

            if is_new:
                st.success(f"Warlord {warlord.epithet} successfully appointed")

                tg_rest_message = TgRestWarlordAppointment(user.id, warlord.id, duration)
                send_tg_rest(tg_rest_message)
            else:
                st.success(f"Warlord {warlord.epithet} successfully updated")
        except Exception as e:
            st.error(f"Error saving Warlord: {e}")
    except ValidationException as ve:
        st.error(ve)
