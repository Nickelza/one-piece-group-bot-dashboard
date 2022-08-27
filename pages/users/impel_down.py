from datetime import datetime

import streamlit as st

from src.model.User import User
from src.model.exceptions.ValidationException import ValidationException
from src.service.tg_rest_service import send_tg_rest_message, escape_valid_markdown_chars
from src.service.time_service import get_remaining_time


def main(user: User) -> None:
    """
    Impel down function
    :return:
    """
    key_suffix = "_impel_down"

    # Display arrested status
    if user.is_arrested():
        arrested_status_text = "Arrested"
        if user.impel_down_is_permanent:
            arrested_status_text += " (permanent)"
        else:
            arrested_status_text += " until {}".format(user.impel_down_release_date)
    else:
        arrested_status_text = "Free"
    st.info(arrested_status_text)

    # Impel down status form
    with st.form(f"impel_down_form_{user.id}{key_suffix}"):
        # Sentence type  radio
        if user.impel_down_is_permanent:
            sentence_radio_index = 2
        elif user.is_arrested():
            sentence_radio_index = 1
        else:
            sentence_radio_index = 0

        sentence_type = st.radio("Sentence", ["None", "Temporary", "Permanent"], index=sentence_radio_index,
                                 key=f"sentence_radio_{user.id}{key_suffix}")

        # Release date and time
        col_release_date, col_release_time = st.columns(2)
        release_date = col_release_date.date_input("Release date", value=user.impel_down_release_date,
                                                   key=f"release_date_{user.id}{key_suffix}")
        release_time = col_release_time.time_input("Release time", value=user.impel_down_release_date,
                                                   key=f"release_time_{user.id}{key_suffix}")

        # Bounty action radio
        bounty_action = st.radio("Bounty action", ["None", "Halve", "Erase"],
                                 key=f"bounty_action_{user.id}{key_suffix}")

        # Send message checkbox
        should_send_message = st.checkbox("Send message", key=f"send_message_{user.id}{key_suffix}")

        # Reason input
        reason = st.text_input("Reason", key=f"reason_{user.id}{key_suffix}")

        # Save button
        submitted = st.form_submit_button("Save")

        if submitted:
            save(user, sentence_type, bounty_action, release_date, release_time, should_send_message, reason)


def save(user: User, sentence_type: str, bounty_action: str, release_date: datetime,
         release_time: datetime.time, should_send_message, reason) -> None:
    """
    Save impel down status
    :param user: User
    :param sentence_type: Sentence type
    :param bounty_action: Bounty action
    :param release_date: Release date
    :param release_time: Release time
    :param should_send_message: If a message should be sent
    :param reason: Reason. Must be set if should_send_message is True
    :return:
    """
    try:
        # Validation
        validate(sentence_type, release_date, release_time, should_send_message, reason)

        # Save
        user.impel_down_is_permanent = sentence_type == "Permanent"

        if sentence_type == "None" or sentence_type == "Permanent":
            user.impel_down_release_date = None
        else:
            user.impel_down_release_date = datetime.combine(release_date, release_time)

        if bounty_action == "Halve":
            user.bounty = user.bounty // 2
        elif bounty_action == "Erase":
            user.bounty = 0
        user.save()
        st.success("Saved")

        # Send notification message
        if should_send_message:
            notification_message = get_notification_message(sentence_type, datetime.combine(release_date, release_time),
                                                            bounty_action, reason)
            send_tg_rest_message(user, notification_message)

    except ValidationException as ve:
        st.error(ve)
        return


def validate(sentence_type: str, release_date: datetime, release_time: datetime.time, should_send_message: bool,
             reason: str) -> None:
    """
    Validate impel down status
    :param sentence_type: Sentence type
    :param release_date: Release date
    :param release_time: Release time
    :param should_send_message: If a message should be sent
    :param reason: Reason. Must be set if should_send_message is True
    :return:
    """

    # If sentence is temporary, release date and time must be in the future
    if sentence_type == "Temporary":
        release_date_time = datetime.combine(release_date, release_time)
        if release_date < datetime.now().date():
            raise ValidationException("Release date cannot be earlier than today")
        if release_date_time < datetime.now():
            raise ValidationException("Release time cannot be earlier than now")

    # If you should send message sentence and type is not None, reason must be set
    if should_send_message and sentence_type != "None":
        if reason == "":
            raise ValidationException("Reason must be set if should send message is checked")


def get_notification_message(sentence_type: str, release_date_time: datetime, bounty_action: str, reason: str) -> str:
    """
    Get notification message
    :param sentence_type: Sentence type
    :param release_date_time: Release date and time
    :param bounty_action: Bounty action
    :param reason: Reason
    :return:
    """

    if sentence_type == "None" and bounty_action == "None":
        return "Your disciplinary action has been lifted"

    text = "⛔Disciplinary action"

    if reason != "":
        text += "\n\n*Reason*: " + escape_valid_markdown_chars(reason)

    text += "\n\n*Restrictions*:"

    if bounty_action == "Halve":
        text += "\n- Bounty halved"
    elif bounty_action == "Erase":
        text += "\n- Bounty erased"

    if sentence_type == "Temporary" or sentence_type == "Permanent":
        text += "\n- You can't acquire any new bounty"
        text += "\n- You can't appear in the leaderboard"
        text += "\n- You can't challenge other users or play games"
        text += "\n- You can't bet in polls"

    text += "\n\n*Duration*: "

    if sentence_type == "Temporary":
        text += get_remaining_time(release_date_time)
    else:
        text += "Permanent"

    return text
