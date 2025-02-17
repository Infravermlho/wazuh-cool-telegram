import streamlit as st
from streamlit import session_state as state


def DefaultAlert(default_alert):
    top_row = st.columns([1, 1, 1, 1, 1, 1])
    with top_row[0]:
        st.text_input(
            "Titulo",
            value=default_alert["title"],
            key="d_title",
        )

    with top_row[1]:
        st.text_input(
            "ID da Regra",
            value=default_alert["rule_id"],
            key="d_rule_id",
        )

    with top_row[2]:
        st.text_input(
            "Client",
            value=default_alert["client"],
            key="d_client",
        )

    with top_row[3]:
        st.text_input(
            "Email Copia",
            value=default_alert["cc"],
            key="d_cc",
        )

    with top_row[4]:
        st.text_input(
            "Categoria",
            value=default_alert["category"],
            key="d_category",
        )

    with top_row[5]:
        st.text_input(
            "Minimo de N minutos entre ações",
            value=default_alert["min_action_interval_minutes"],
            key="d_min_action_interval_minutes",
        )

    middle_row = st.columns([1, 1, 1, 1, 1, 1])
    with middle_row[0]:
        st.text_input(
            "Referencia",
            value=default_alert["reference"],
            key="d_reference",
        )

    with middle_row[1]:
        st.text_input(
            "Urgencia",
            value=default_alert["urgency"],
            key="d_urgency",
        )

    with middle_row[2]:
        st.text_input(
            "Status",
            value=default_alert["status"],
            key="d_status",
        )

    with middle_row[3]:
        st.text_input(
            "Created by",
            value=default_alert["created_by"],
            key="d_created_by",
        )

    with middle_row[4]:
        st.text_input(
            "Service",
            value=default_alert["service"],
            key="d_service",
        )

    with middle_row[5]:
        st.text_input(
            "Inativo em N minutos",
            value=default_alert["inactive_in_minutes"],
            key="d_inactive_in_minutes",
        )

    bottom_row = st.columns(4)
    with bottom_row[0]:
        st.text_area(
            "Descrição",
            height=125,
            value=default_alert["description"],
            key="d_description",
        )
    with bottom_row[1]:
        st.text_area(
            "Descrição Detalhada",
            height=125,
            value=default_alert["detailed_description"],
            key="d_detailed_description",
        )
    with bottom_row[2]:
        st.text_area(
            "Comentarios",
            height=125,
            value=default_alert["comment"],
            key="d_comment",
        )
    with bottom_row[3]:
        st.text_area(
            "Recomendações",
            height=125,
            value=default_alert["recommendation"],
            key="d_recommendation",
        )


def Alert(alert):
    index = alert["id"]

    if f"rule_id{index}" in state:
        title = state[f"rule_id{index}"]
    else:
        title = alert["rule_id"]

    if index > state.starting_index:
        st.markdown(f"## :red[Regra: {title}]")
    else:
        st.markdown(f"## Regra: {title}")

    # -----
    top_row = st.columns([1, 1, 1, 1, 1, 1])
    with top_row[0]:
        st.text_input(
            "Titulo",
            value=alert["title"],
            key=f"title{index}",
            placeholder=state["d_title"],
        )

    with top_row[1]:
        st.text_input(
            "ID da Regra",
            value=alert["rule_id"],
            key=f"rule_id{index}",
            placeholder=state["d_rule_id"],
        )

    with top_row[2]:
        st.text_input(
            "Client",
            value=alert["client"],
            key=f"client{index}",
            placeholder=state["d_client"],
        )

    with top_row[3]:
        st.text_input(
            "Email Copia",
            value=alert["cc"],
            key=f"cc{index}",
            placeholder=state["d_cc"],
        )

    with top_row[4]:
        st.text_input(
            "Categoria",
            value=alert["category"],
            key=f"category{index}",
            placeholder=state["d_category"],
        )

    with top_row[5]:
        st.text_input(
            "Minimo de N minutos entre ações",
            value=alert["min_action_interval_minutes"],
            key=f"min_action_interval_minutes{index}",
            placeholder=state["d_min_action_interval_minutes"],
        )

    middle_row = st.columns([1, 1, 1, 1, 1, 1])
    with middle_row[0]:
        st.text_input(
            "Referencia",
            value=alert["reference"],
            key=f"reference{index}",
            placeholder=state["d_reference"],
        )

    with middle_row[1]:
        st.text_input(
            "Urgencia",
            value=alert["urgency"],
            key=f"urgency{index}",
            placeholder=state["d_urgency"],
        )

    with middle_row[2]:
        st.text_input(
            "Status",
            value=alert["status"],
            key=f"status{index}",
            placeholder=state["d_status"],
        )

    with middle_row[3]:
        st.text_input(
            "Created by",
            value=alert["created_by"],
            key=f"created_by{index}",
            placeholder=state["d_created_by"],
        )

    with middle_row[4]:
        st.text_input(
            "Service",
            value=alert["service"],
            key=f"service{index}",
            placeholder=state["d_service"],
        )

    with middle_row[5]:
        st.text_input(
            "Inativo em N minutos",
            value=alert["inactive_in_minutes"],
            key=f"inactive_in_minutes{index}",
            placeholder=state["d_inactive_in_minutes"],
        )

    bottom_row = st.columns(4)

    with bottom_row[0]:
        st.text_area(
            "Descrição",
            height=125,
            value=alert["description"],
            key=f"description{index}",
            placeholder=state["d_description"],
        )

    with bottom_row[1]:
        st.text_area(
            "Descrição Detalhada",
            height=125,
            value=alert["detailed_description"],
            key=f"detailed_description{index}",
            placeholder=state["d_detailed_description"],
        )

    with bottom_row[2]:
        st.text_area(
            "Comentarios",
            height=125,
            value=alert["comment"],
            key=f"comment{index}",
            placeholder=state["d_comment"],
        )

    with bottom_row[3]:
        st.text_area(
            "Recomendações",
            height=125,
            value=alert["recommendation"],
            key=f"recommendation{index}",
            placeholder=state["d_recommendation"],
        )
