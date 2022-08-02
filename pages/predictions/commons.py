from datetime import datetime

import streamlit as st

import resources.Environment as Env
from src.model.Prediction import Prediction
from src.model.PredictionOption import PredictionOption
from src.model.enums.PredictionStatus import PredictionStatus
from src.model.enums.PredictionType import PredictionType
from src.model.exceptions.ValidationException import ValidationException


def get_add_form_optionals(key_suffix: str, prediction: Prediction = None, prediction_options: list = None
                           ) -> (int, bool, bool, bool, datetime.time):
    """
    Gets the add form optionals
    :param key_suffix: Key suffix
    :param prediction: If not None, values from the prediction are autofilled
    :param prediction_options: If not None, values from the prediction options are autofilled
    :return: (options_count, should_send, should_end, default_time_value)
    """

    prediction_status = PredictionStatus(prediction.status) if prediction is not None else None
    is_sent = prediction is not None and prediction_status >= PredictionStatus.SENT
    is_closed = prediction is not None and prediction_status >= PredictionStatus.BETS_CLOSED

    options_count = st.slider('How many options', 2, 10, key=f"options_count{key_suffix}",
                              value=(2 if prediction_options is None else len(prediction_options)),
                              disabled=is_sent)

    should_cut_off = False
    # Show cut_off checkbox if prediction is sent
    if prediction_status is not None and prediction_status is not PredictionStatus.NEW:
        col_1, col_2, col_3 = st.columns(3)

        should_cut_off = col_3.checkbox('Cut off Bets', key=f"should_cut_off{key_suffix}",
                                        value=(False if (prediction is None or prediction.cut_off_date is None)
                                               else True), disabled=is_closed)
    else:
        col_1, col_2 = st.columns(2)

    should_send = col_1.checkbox('Schedule send', key=f"should_send{key_suffix}",
                                 value=(False if (prediction is None or prediction.send_date is None) else True),
                                 disabled=is_sent)

    should_end = col_2.checkbox('Schedule end', key=f"should_end{key_suffix}",
                                value=(False if (prediction is None or prediction.end_date is None) else True),
                                disabled=is_closed)

    default_time_value = datetime.strptime("11:00", '%H:%M').time()

    return options_count, should_send, should_end, should_cut_off, default_time_value


def get_add_form(options_count: int, should_send: bool, should_end: bool, should_cut_off,
                 default_time_value: datetime.time, key_suffix: str, prediction: Prediction = None,
                 prediction_options: list = None) -> None:
    """
    Gets the prediction add form
    :param options_count: Number of options
    :param should_send: Should send
    :param should_end: Should end
    :param should_cut_off: Should cut_off
    :param default_time_value: Default time value
    :param key_suffix: Key suffix
    :param prediction: If not None, values from the prediction are autofilled
    :param prediction_options: If not None, values from the prediction options are autofilled
    :return: None
    """

    prediction_status: PredictionStatus = PredictionStatus(prediction.status) if prediction is not None else None
    is_sent = prediction is not None and prediction_status >= PredictionStatus.SENT
    is_closed = prediction is not None and prediction_status >= PredictionStatus.BETS_CLOSED

    # Type
    prediction_types = [p.value for p in PredictionType]
    st.selectbox("Prediction Type", prediction_types, key=f"prediction_type{key_suffix}",
                 index=(0 if prediction is None else prediction_types.index(prediction.type)), disabled=is_sent)

    # Question
    st.text_input("Question", key=f"question{key_suffix}",
                  value=(prediction.question if prediction is not None else ""), disabled=is_sent)

    # Options
    for i in range(options_count):
        option_value = prediction_options[i].option if (
                prediction is not None and i < len(prediction_options)) else ""

        option_description = f"Option {i + 1}"
        if prediction is not None and PredictionStatus(prediction.status) is PredictionStatus.RESULT_SET:
            prediction_option: PredictionOption = prediction_options[i]
            if prediction_option.is_correct:
                option_description += " ✅"
        st.text_input(option_description, key=f"option_{i}{key_suffix}", value=option_value, disabled=is_sent)

    col_1, col_2, col_3 = st.columns(3)

    # Should refund berry
    col_1.checkbox("Refund wager", key=f"refund_wager{key_suffix}",
                   value=(Env.REFUND_WAGER_DEFAULT.get_bool() if prediction is None else prediction.refund_wager),
                   disabled=is_closed)

    # Should allow multiple choices
    col_2.checkbox("Allow multiple choices", key=f"multiple_choices{key_suffix}",
                   value=(Env.ALLOW_MULTIPLE_CHOICES_DEFAULT.get_bool() if prediction is None
                          else prediction.allow_multiple_choices), disabled=is_closed)

    # Should allow bets withdrawal
    col_3.checkbox("Allow bets withdrawal", key=f"can_withdraw_bet{key_suffix}",
                   value=(Env.CAN_WITHDRAW_BET_DEFAULT.get_bool() if prediction is None
                          else prediction.can_withdraw_bet), disabled=is_closed)

    col_1, col_2 = st.columns(2)
    # Schedule send
    if should_send:
        send_date = prediction.send_date if prediction is not None else datetime.now()
        send_time = prediction.send_date if prediction is not None else default_time_value
        col_1.date_input("Send Date", key=f"send_date{key_suffix}", value=send_date, disabled=is_sent)
        col_2.time_input("Send Time", key=f"send_time{key_suffix}", value=send_time, disabled=is_sent)

    col_1, col_2 = st.columns(2)
    # Schedule end
    if should_end:
        end_date = prediction.end_date if prediction is not None else datetime.now()
        end_time = prediction.end_date if prediction is not None else default_time_value
        col_1.date_input("End Date", key=f"end_date{key_suffix}", value=end_date, disabled=is_closed)
        col_2.time_input("End Time", key=f"end_time{key_suffix}", value=end_time, disabled=is_closed)

    col_1, col_2 = st.columns(2)
    # Schedule cut_off
    if should_cut_off:
        cut_off_date = prediction.cut_off_date if prediction is not None else datetime.now()
        cut_off_time = prediction.cut_off_date if prediction is not None else default_time_value
        col_1.date_input("Cut off Bets Date", key=f"cut_off_date{key_suffix}", value=cut_off_date,
                         disabled=is_closed)
        col_2.time_input("Cut Off Bets Time", key=f"cut_off_time{key_suffix}", value=cut_off_time,
                         disabled=is_closed)


def validate(key_suffix: str, prediction: Prediction) -> None:
    """
    Validate function. Raises an exception if form is not valid
    :param key_suffix: Key suffix
    :param prediction: The prediction
    :return:
    """

    prediction_status: PredictionStatus = PredictionStatus(prediction.status) if prediction is not None else None
    is_sent = prediction is not None and prediction_status >= PredictionStatus.SENT
    is_closed = prediction is not None and prediction_status >= PredictionStatus.BETS_CLOSED

    if get_session_state_key("question", key_suffix) == "":
        raise ValidationException("Question is required")

    for i in range(get_session_state_key("options_count", key_suffix)):
        if get_session_state_key(f"option_{i}{key_suffix}", key_suffix) == "":
            raise ValidationException(f"Option {i + 1} is required")

    should_send = get_session_state_key("should_send", key_suffix)
    should_send_datetime = None  # To silence IDE warning

    # If not already sent, validate send date and time
    if should_send:
        should_send_datetime = datetime.combine(get_session_state_key("send_date", key_suffix),
                                                get_session_state_key("send_time", key_suffix))

        if not is_sent:
            if get_session_state_key("send_date", key_suffix) < datetime.now().date():
                raise ValidationException("Send date cannot be earlier than today")

            if should_send_datetime < datetime.now():
                raise ValidationException("Send time cannot be earlier than now")

    # If not already closed, validate end date and time
    if get_session_state_key("should_end", key_suffix) and not is_closed:
        if get_session_state_key("end_date", key_suffix) < datetime.now().date():
            raise ValidationException("End date cannot be earlier than today")

        should_end_datetime = datetime.combine(get_session_state_key("end_date", key_suffix),
                                               get_session_state_key("end_time", key_suffix))
        if should_end_datetime < datetime.now():
            raise ValidationException("End time cannot be earlier than now")

        if should_send and should_end_datetime <= should_send_datetime:
            raise ValidationException("End time must be later than send time")

    # If not already closed, validate cut off date and time
    if get_session_state_key("should_cut_off", key_suffix) and not is_closed:
        should_cut_off_datetime = datetime.combine(get_session_state_key("cut_off_date", key_suffix),
                                                   get_session_state_key("cut_off_time", key_suffix))

        if should_cut_off_datetime > datetime.now():
            raise ValidationException("Cut off time cannot be later than now")

        if should_cut_off_datetime <= should_send_datetime:
            raise ValidationException("Cut off time must be later than send time")


def get_session_state_key(key: str, suffix: str) -> any:
    """
    Gets the session state key
    :param key: Key
    :param suffix: Suffix
    :return: Session state key
    """

    return st.session_state.get(f"{key}{suffix}")


def save(options_count: int, key_suffix: str, prediction: Prediction = None, prediction_options: list = None) -> None:
    """
    Saves the prediction
    :param options_count: Number of options
    :param key_suffix: Key suffix
    :param prediction: If not None, the prediction is updated
    :param prediction_options: If not None, the prediction options are updated
    :return: None
    """

    is_new = prediction is None
    # Save prediction
    if is_new:
        prediction: Prediction = Prediction()

    try:
        validate(key_suffix, prediction)
        try:
            # Type
            prediction.type = get_session_state_key("prediction_type", key_suffix)

            # Question
            prediction.question = get_session_state_key("question", key_suffix)

            # Scheduled send date
            prediction.send_date = datetime.combine(get_session_state_key("send_date", key_suffix),
                                                    get_session_state_key("send_time", key_suffix)) \
                if get_session_state_key("send_date", key_suffix) is not None else None

            # Scheduled end date
            prediction.end_date = datetime.combine(get_session_state_key("end_date", key_suffix),
                                                   get_session_state_key("end_time", key_suffix)) \
                if get_session_state_key("end_date", key_suffix) is not None else None

            # Scheduled cut_off date
            prediction.cut_off_date = datetime.combine(get_session_state_key("cut_off_date", key_suffix),
                                                       get_session_state_key("cut_off_time", key_suffix)) \
                if get_session_state_key("cut_off_date", key_suffix) is not None else None

            prediction.refund_wager = get_session_state_key("refund_wager", key_suffix)
            prediction.allow_multiple_choices = get_session_state_key("multiple_choices", key_suffix)
            prediction.can_withdraw_bet = get_session_state_key("can_withdraw_bet", key_suffix)

            prediction.save()

            # Save options
            should_save_options = True
            options_form = [get_session_state_key("option", f"_{i}{key_suffix}") for i in range(options_count)]
            # In case of already existing prediction, delete all options if they are different
            if not is_new:
                options_saved = [option.option for option in prediction_options]
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
