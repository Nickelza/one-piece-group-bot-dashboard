from datetime import datetime

import streamlit as st

from src.model.Prediction import Prediction
from src.model.PredictionOption import PredictionOption
from src.model.enums.PredictionStatus import PredictionStatus
from src.model.enums.PredictionType import PredictionType
from src.model.exceptions.ValidationException import ValidationException


def get_add_form_optionals(key_suffix: str, prediction: Prediction = None) -> (int, bool, bool, datetime.time):
    """
    Gets the add form optionals
    :param key_suffix: Key suffix
    :param prediction: If not None, values from the prediction are autofilled
    :return: (options_count, should_send, should_end, default_time_value)
    """

    is_sent = prediction is not None and PredictionStatus(prediction.status) >= PredictionStatus.SENT
    is_accepting_bets = prediction is not None and PredictionStatus(prediction.status) <= PredictionStatus.BETS_CLOSED

    options_count = st.slider('How many options', 2, 10, key=f"options_count{key_suffix}",
                              value=(2 if prediction is None else len(prediction.prediction_options)),
                              disabled=is_sent)

    col_1, col_2 = st.columns(2)

    should_send = col_1.checkbox('Schedule send', key=f"should_send{key_suffix}",
                                 value=(False if (prediction is None or prediction.send_date is None) else True),
                                 disabled=is_sent)

    should_end = col_2.checkbox('Schedule end', key=f"should_end{key_suffix}",
                                value=(False if (prediction is None or prediction.end_date is None) else True),
                                disabled=(not is_accepting_bets))

    default_time_value = datetime.strptime("11:00", '%H:%M').time()

    return options_count, should_send, should_end, default_time_value


def get_add_form(options_count: int, should_send: bool, should_end: bool, default_time_value: datetime.time,
                 key_suffix: str, prediction: Prediction = None) -> None:
    """
    Gets the prediction add form
    :param options_count: Number of options
    :param should_send: Should send
    :param should_end: Should end
    :param default_time_value: Default time value
    :param key_suffix: Key suffix
    :param prediction: If not None, values from the prediction are autofilled
    :return: None
    """

    is_sent = prediction is not None and PredictionStatus(prediction.status) >= PredictionStatus.SENT
    is_accepting_bets = prediction is not None and PredictionStatus(prediction.status) <= PredictionStatus.BETS_CLOSED

    # Type
    prediction_types = [p.value for p in PredictionType]
    st.selectbox("Prediction Type", prediction_types, key=f"prediction_type{key_suffix}",
                 index=(0 if prediction is None else prediction_types.index(prediction.type)), disabled=is_sent)

    # Question
    st.text_input("Question", key=f"question{key_suffix}",
                  value=(prediction.question if prediction is not None else ""), disabled=is_sent)

    # Options
    for i in range(options_count):
        option_value = prediction.prediction_options[i].option if (
                prediction is not None and i < len(prediction.prediction_options)) else ""

        option_description = f"Option {i + 1}"
        if prediction is not None and PredictionStatus(prediction.status) is PredictionStatus.RESULT_SET:
            prediction_option: PredictionOption = prediction.prediction_options[i]
            if prediction_option.is_correct:
                option_description += " ✅"
        st.text_input(option_description, key=f"option_{i}{key_suffix}", value=option_value, disabled=is_sent)

    col_1, col_2 = st.columns(2)

    # Should refund berry
    col_1.checkbox("Refund wager", key=f"refund_wager{key_suffix}",
                   value=(True if prediction is None else prediction.refund_wager), disabled=is_sent)

    # Should allow multiple choices
    col_2.checkbox("Allow multiple choices", key=f"multiple_choices{key_suffix}",
                   value=(True if prediction is None else prediction.allow_multiple_choices), disabled=is_sent)

    # Schedule send
    if should_send:
        send_date = prediction.send_date if prediction is not None else datetime.now()
        col_1.date_input("Send Date", key=f"send_date{key_suffix}", value=send_date, disabled=is_sent)
        col_2.time_input("Send Time", key=f"send_time{key_suffix}", value=default_time_value, disabled=is_sent)

    # Schedule end
    if should_end:
        end_date = prediction.end_date if prediction is not None else datetime.now()
        col_1.date_input("End Date", key=f"end_date{key_suffix}", value=end_date, disabled=(not is_accepting_bets))
        col_2.time_input("End Time", key=f"end_time{key_suffix}", value=default_time_value,
                         disabled=(not is_accepting_bets))


def validate(key_suffix: str) -> None:
    """
    Validate function. Raises an exception if form is not valid.
    :param key_suffix: Key suffix
    :return:
    """

    if get_session_state_key("question", key_suffix) == "":
        raise ValidationException("Question is required")

    for i in range(get_session_state_key("options_count", key_suffix)):
        if get_session_state_key(f"option_{i}{key_suffix}", key_suffix) == "":
            raise ValidationException(f"Option {i + 1} is required")

    should_send = get_session_state_key("should_send", key_suffix)
    should_send_datetime = None  # To silence IDE warning
    if should_send:
        should_send_datetime = datetime.combine(get_session_state_key("send_date", key_suffix),
                                                get_session_state_key("send_time", key_suffix))

        if get_session_state_key("send_date", key_suffix) < datetime.now().date():
            raise ValidationException("Send date cannot be earlier than today")

        if should_send_datetime < datetime.now():
            raise ValidationException("Send time cannot be earlier than now")

    if get_session_state_key("should_end", key_suffix):
        if get_session_state_key("end_date", key_suffix) < datetime.now().date():
            raise ValidationException("End date cannot be earlier than today")

        should_end_datetime = datetime.combine(get_session_state_key("end_date", key_suffix),
                                               get_session_state_key("end_time", key_suffix))
        if should_end_datetime < datetime.now():
            raise ValidationException("End time cannot be earlier than now")

        if should_send and should_end_datetime <= should_send_datetime:
            raise ValidationException("End time must be later than send time")


def get_session_state_key(key: str, suffix: str) -> any:
    """
    Gets the session state key
    :param key: Key
    :param suffix: Suffix
    :return: Session state key
    """

    return st.session_state.get(f"{key}{suffix}")


def save(should_send: bool, should_end: bool, options_count: int, key_suffix: str,
         prediction: Prediction = None) -> None:
    """
    Saves the prediction
    :param should_send: Should send
    :param should_end: Should end
    :param options_count: Number of options
    :param key_suffix: Key suffix
    :param prediction: If not None, the prediction is updated
    :return: None
    """

    is_new = prediction is None
    # Save prediction
    if is_new:
        prediction: Prediction = Prediction()

    try:
        validate(key_suffix)
        try:
            prediction.type = get_session_state_key("prediction_type", key_suffix)
            prediction.question = get_session_state_key("question", key_suffix)
            prediction.send_date = datetime.combine(get_session_state_key("send_date", key_suffix),
                                                    get_session_state_key("send_time", key_suffix)) \
                if should_send else None

            prediction.end_date = datetime.combine(get_session_state_key("end_date", key_suffix),
                                                   get_session_state_key("end_time", key_suffix)) \
                if should_end else None

            prediction.refund_wager = get_session_state_key("refund_wager", key_suffix)
            prediction.allow_multiple_choices = get_session_state_key("multiple_choices", key_suffix)

            prediction.save()

            # Save options
            should_save_options = True
            options_form = [get_session_state_key("option", f"_{i}{key_suffix}") for i in range(options_count)]
            # In case of already existing prediction, delete all options if they are different
            if not is_new:
                options_saved = [option.option for option in prediction.prediction_options]
                if options_form != options_saved:
                    PredictionOption.delete().where(PredictionOption.prediction == prediction).execute()
                else:
                    should_save_options = False

            if should_save_options:
                for i in range(options_count):
                    prediction_option = PredictionOption()
                    prediction_option.prediction = prediction
                    prediction_option.option = options_form[i]
                    prediction_option.save()

            st.success("Prediction saved" if is_new else "Prediction updated")
        except Exception as e:
            st.error(e)

    except ValidationException as ve:
        st.error(ve.message)


