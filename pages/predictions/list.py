import logging

import streamlit as st

from pages.predictions.commons import get_add_form_optionals, get_add_form, save, get_session_state_key
from src.model.Prediction import Prediction
from src.model.PredictionOption import PredictionOption
from src.model.enums.PredictionStatus import PredictionStatus


def main() -> None:
    """
    View list function
    :return:
    """

    st.subheader("List")
    key_suffix = "_list"
    predictions: list[Prediction] = Prediction.select()
    for index, prediction in enumerate(predictions):
        key_suffix_list = f"{key_suffix}_{index}"

        with st.expander(prediction.question):
            prediction_options = prediction.prediction_options
            options_count, should_send, should_end, default_time_value = \
                get_add_form_optionals(key_suffix_list, prediction=prediction, prediction_options=prediction_options)

            with st.form(f"prediction_edit_form{key_suffix_list}", clear_on_submit=False):
                get_add_form(options_count, should_send, should_end, default_time_value, key_suffix_list,
                             prediction=prediction, prediction_options=prediction_options)
                submitted = st.form_submit_button("Save edit")

                if submitted:
                    save(should_send, should_end, options_count, key_suffix_list, prediction=prediction,
                         prediction_options=prediction_options)

            correct_options_container = st.container()
            cols_send_delete = st.columns(2)
            cols_close_set_results = st.columns(1)
            # New prediction, show send and delete buttons
            if PredictionStatus(prediction.status) is PredictionStatus.NEW:
                cols_send_delete[0].button("Send", key=f"send{key_suffix_list}", on_click=send, args=[prediction])
                cols_send_delete[1].button("Delete", key=f"delete{key_suffix_list}", on_click=delete, args=[prediction])

            # Sent prediction, show close bets button
            elif PredictionStatus(prediction.status) is PredictionStatus.SENT:
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

            elif PredictionStatus(prediction.status) is PredictionStatus.RESULT_SET:
                st.info("Prediction closed")


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

    logging.info(f"Prediction {prediction.id} sent")
    prediction.status = PredictionStatus.SENT.value
    prediction.save()
    st.success("Prediction sent")


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

    # FIXME remove comment
    # prediction.delete_instance()
    st.success("Prediction deleted")


def close_bets(prediction: Prediction) -> None:
    """
    Close bets function
    :param prediction: Prediction
    :return:
    """

    logging.info(f"Prediction {prediction.id} closed")
    prediction.status = PredictionStatus.BETS_CLOSED.value
    prediction.save()
    st.success("Bets closed")


def set_results(prediction: Prediction, key_suffix: str) -> None:
    """
    Set results function
    :param prediction: Prediction
    :param key_suffix: Key suffix
    :return:
    """

    logging.info(f"Prediction {prediction.id} results set")

    # Save correct options
    correct_options = get_session_state_key("correct_options", key_suffix)
    for correct_option in correct_options:
        prediction_option = prediction.prediction_options.filter(PredictionOption.option == correct_option).first()
        prediction_option.is_correct = True
        prediction_option.save()

    prediction.status = PredictionStatus.RESULT_SET.value
    prediction.save()

    st.success("Results set")
