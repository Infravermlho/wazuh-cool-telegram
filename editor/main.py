import os
import shutil
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
from streamlit import session_state as state

import components.AlertComponents as alerts

EMPRESA = os.getenv("EMPRESA", "placeholder")
CSV_PATH = os.getenv("CSV_PATH", "./dev.csv")
BACKUPS_PATH = os.getenv("BACKUPS_PATH", "./")


def load_default():
    df_default = pd.read_csv(CSV_PATH, nrows=1)

    # temp fix
    if "min_action_interval_minutes" not in df_default:
        df_default["min_action_interval_minutes"] = 0

    dict_default = df_default.replace(np.nan, None).to_dict("records")[0]

    return df_default, dict_default


def load_alerts():
    df_alerts = pd.read_csv(CSV_PATH, skiprows=[1])
    df_alerts = df_alerts.sort_values(by=["rule_id"], ascending=False)
    print(df_alerts)

    if "min_action_interval_minutes" not in df_alerts:
        df_alerts["min_action_interval_minutes"] = None

    df_alerts["id"] = df_alerts.index

    dict_alerts = df_alerts.replace(np.nan, None).to_dict("records")

    return df_alerts, dict_alerts


def create_alerts():
    state.total_index += 1
    state.dict_alerts.insert(
        0, {x: None for x in state.dict_default} | {"id": state.total_index}
    )
    state.current_page = 1
    state.loading = True


def delete_alert(index):
    state.dict_alerts = [alert for alert in state.dict_alerts if alert["id"] != index]
    state.loading = True


def apply_changes():
    data = [[key for key in state.dict_default]]
    data.append([state[f"d_{key}"] for key in state.dict_default])

    for alert in state.dict_alerts:
        id = alert["id"]
        if f"rule_id{id}" in state:
            data.append([str(state[f"{key}{id}"]) for key in state.dict_default])
        else:
            data.append([str(alert[key]) for key in state.dict_default])

    new_df = pd.DataFrame(data, dtype=str)

    old_path = f"{BACKUPS_PATH}old_{datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}.csv"
    os.makedirs(BACKUPS_PATH, exist_ok=True)
    shutil.copyfile(CSV_PATH, old_path)

    new_df.replace("None", "", inplace=True)
    new_df.fillna("", inplace=True)
    new_df.to_csv(CSV_PATH, header=False, index=False)

    for key in state.keys():
        del state[key]

    st.toast("CSV Atualizado")


def undo_changes():
    for key in state.keys():
        del state[key]

    st.toast("Mudanças descartadas")


st.set_page_config(
    layout="wide",
    page_title=f"Editor de Alertas • {EMPRESA}",
    page_icon="🧮",
)

st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""",
    unsafe_allow_html=True,
)

st.title("Gerenciador de Alertas Movidesk")

if "df_default" not in state:
    df_default, dict_default = load_default()
    state["df_default"] = df_default
    state["dict_default"] = dict_default

if "df_alerts" not in state:
    df_alerts, dict_alerts = load_alerts()
    state["df_alerts"] = df_alerts
    state["dict_alerts"] = dict_alerts
    state["starting_index"] = len(dict_alerts) - 1
    state["total_index"] = state.starting_index


st.markdown(f"### {EMPRESA}")
st.markdown(f"## Alerta Default")
alerts.DefaultAlert(state.dict_default)
st.markdown(f"---")


if "loading" not in state:
    state.loading = True


st.button(
    "Criar Alerta",
    use_container_width=True,
    disabled=state.loading,
    type="primary",
    on_click=create_alerts,
)

row = st.columns(2)
row[0].button(
    ":red-background[Desfazer Mudanças]",
    disabled=state.loading,
    use_container_width=True,
    type="secondary",
    on_click=undo_changes,
)

row[1].button(
    ":green-background[Aplicar Mudanças]",
    disabled=state.loading,
    use_container_width=True,
    type="secondary",
    on_click=apply_changes,
)

st.markdown(f"## Alertas")

progress_bar = st.progress(0, text="Buscando alertas")
display_alertas = st.container()

bottom_menu = st.columns((4, 1, 1))
with bottom_menu[2]:
    batch_size = st.selectbox("Tamanho da Pagina", options=[5, 10, 25])
with bottom_menu[1]:
    total_pages = (
        int(len(state.dict_alerts) / batch_size)
        if int(len(state.dict_alerts) / batch_size) > 0
        else 1
    )
    current_page = st.number_input(
        "Pagina", min_value=1, key="current_page", max_value=total_pages, step=1
    )
with bottom_menu[0]:
    st.markdown(f"Pagina **{current_page}** de **{total_pages}** ")


with display_alertas:
    for index, alert in enumerate(
        state.dict_alerts[batch_size * (current_page - 1) : batch_size * current_page]
    ):
        with st.container(border=True):
            alerts.Alert(alert)

            st.button(
                "Deletar Alerta",
                key=f"delete{alert["id"]}",
                use_container_width=True,
                args=(alert["id"],),
                on_click=delete_alert,
            )

        progress_bar.progress(
            int(index / len(state.dict_alerts) * 100), text="Buscando alertas"
        )

progress_bar.empty()


if state["loading"]:
    state["loading"] = False
    st.rerun()
