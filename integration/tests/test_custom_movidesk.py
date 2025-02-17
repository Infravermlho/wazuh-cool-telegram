"""
Testa o script sem necessidade de gerar alerta no wazuh
"""

import importlib
import os

from dotenv import load_dotenv

custom_movidesk = importlib.import_module("../custom-good-telegram.py")

load_dotenv(dotenv_path=".env.secret")

API_KEY = os.getenv(
    "API_KEY",
    input(".env.secret com chave de API não encontrado, inserir manualmente?:"),
)


if API_KEY:
    custom_movidesk.main(
        "/usr/share/wazuh-good-telegram/",  # use cases path
        "tests/test.log",  # log file path
        "tests/101007.json",  # alert json data
        API_KEY,
    )
else:
    print("Arquivo .env.secret com a chave API_KEY não encontrado")
