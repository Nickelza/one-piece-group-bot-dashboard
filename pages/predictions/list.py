import streamlit as st

from pages.predictions.commons import get_add_form_optionals, get_add_form, save, get_session_state_key
from src.model.Prediction import Prediction
from src.model.PredictionOption import PredictionOption
from src.model.enums.PredictionStatus import PredictionStatus, get_all_prediction_status_names, \
    get_active_prediction_status_names, get_prediction_status_by_list_of_names, get_prediction_status_name_by_key
from src.model.tgrest.TgBot import TgBot
from src.model.tgrest.TgBot import TgBotRequestException
from src.model.tgrest.TgRestPrediction import TgRestPrediction, TgRestPredictionAction


def main() -> None:
    """
    View list function
    :return:
    """

    key_suffix = "_list"

    # Filter by status multiselect
    status_filter = st.multiselect("Status filter", get_all_prediction_status_names(),
                                   default=get_active_prediction_status_names())
    selected_statuses = get_prediction_status_by_list_of_names(status_filter)

    # Filter by name text input
    question_filter = st.text_input("Question filter", "")

    # Get predictions
    predictions = Prediction.select().where((Prediction.status.in_(selected_statuses))
                                            & (Prediction.question.contains(question_filter)))

    for index, prediction in enumerate(predictions):
        key_suffix_list = f"{key_suffix}_{index}"

        with st.expander(prediction.question):
            st.info(get_prediction_status_name_by_key(prediction.status))
            prediction_options = prediction.prediction_options
            options_count, should_send, should_end, should_cut_off, default_time_value = \
                get_add_form_optionals(key_suffix_list, prediction=prediction, prediction_options=prediction_options)

            with st.form(f"prediction_edit_form{key_suffix_list}", clear_on_submit=False):
                get_add_form(options_count, should_send, should_end, should_cut_off, default_time_value,
                             key_suffix_list, prediction=prediction, prediction_options=prediction_options)
                submitted = st.form_submit_button("Save")

                if submitted:
                    save(options_count, key_suffix_list, prediction=prediction, prediction_options=prediction_options)
                    refresh(prediction)

            correct_options_container = st.container()
            cols_send_delete = st.columns(2)
            cols_close_set_results = st.columns(2)

            # New prediction, show send and delete buttons
            if PredictionStatus(prediction.status) is PredictionStatus.NEW:
                cols_send_delete[0].button("Send", key=f"send{key_suffix_list}", on_click=send, args=[prediction])
                cols_send_delete[1].button("Delete", key=f"delete{key_suffix_list}", on_click=delete, args=[prediction])
            else:
                # Sent prediction, show close bets button
                if PredictionStatus(prediction.status) is PredictionStatus.SENT:
                    cols_close_set_results[0].button("Close Bets", key=f"close{key_suffix_list}", on_click=close_bets,
                                                     args=[prediction])

                # Closed bets prediction, show set results button
                elif PredictionStatus(prediction.status) is PredictionStatus.BETS_CLOSED:
                    # Correct options multiselect
                    options = [o.option for o in prediction.prediction_options]
                    correct_options_container.multiselect("Correct options", options,
                                                          key=f"correct_options{key_suffix_list}")

                    cols_close_set_results[0].button("Set Results", key=f"set{key_suffix_list}", on_click=set_results,
                                                     args=[prediction, key_suffix_list])

                cols_close_set_results[1].button("Resend", key=f"delete{key_suffix_list}", on_click=resend,
                                                 args=[prediction])


def send(prediction: Prediction) -> None:
    """
    Send function
    :param prediction: Prediction
    :return:
    """

    # Should never happen because send button would not be visible
    if PredictionStatus(prediction.status) >= PredictionStatus.SENT:
        st.error("This prediction has already been sent")
        return

    send_tg_rest_command(prediction, TgRestPredictionAction.SEND, "Prediction scheduled for sending")


def delete(prediction: Prediction) -> None:
    """
    Delete function
    :param prediction: Prediction
    :return:
    """

    # Should never happen because delete button would not be visible
    if PredictionStatus(prediction.status) >= PredictionStatus.SENT:
        st.error("You can't delete a prediction that has already been sent")
        return

    prediction.delete_instance()
    st.success("Prediction deleted")


def close_bets(prediction: Prediction) -> None:
    """
    Close bets function
    :param prediction: Prediction
    :return:
    """

    # Should never happen because close bets button would not be visible
    if PredictionStatus(prediction.status) >= PredictionStatus.BETS_CLOSED:
        st.error("This prediction has already been closed")
        return

    send_tg_rest_command(prediction, TgRestPredictionAction.CLOSE_BETS, "Prediction scheduled for closing")


def set_results(prediction: Prediction, key_suffix: str) -> None:
    """
    Set results function
    :param prediction: Prediction
    :param key_suffix: Key suffix
    :return:
    """

    # Should never happen because set results button would not be visible
    if PredictionStatus(prediction.status) >= PredictionStatus.RESULT_SET:
        st.error("This prediction results have already been set")
        return

    # Save correct options
    correct_options = get_session_state_key("correct_options", key_suffix)
    for correct_option in correct_options:
        prediction_option = prediction.prediction_options.filter(PredictionOption.option == correct_option).first()
        prediction_option.is_correct = True
        prediction_option.save()

    send_tg_rest_command(prediction, TgRestPredictionAction.SET_RESULTS, "Prediction scheduled for results set")


def refresh(prediction: Prediction) -> None:
    """
    Refresh prediction function
    :param prediction: Prediction
    :return:
    """

    send_tg_rest_command(prediction, TgRestPredictionAction.REFRESH)


def resend(prediction: Prediction) -> None:
    """
    Resend prediction function
    :param prediction: Prediction
    :return:
    """

    send_tg_rest_command(prediction, TgRestPredictionAction.RESEND, "Prediction scheduled for resending")


def send_tg_rest_command(prediction: Prediction, action: TgRestPredictionAction, success_message: str = None) -> None:
    """
    Send tg rest command
    :param prediction: Prediction
    :param action: TgRestPredictionAction
    :param success_message: Success message
    :return:
    """

    # Send command
    tg_rest_prediction = TgRestPrediction(action, prediction.id)

    try:
        TgBot().send_message(tg_rest_prediction)

        if success_message is not None:
            st.success(success_message)
    except TgBotRequestException as e:
        st.error(e.message)
        return
