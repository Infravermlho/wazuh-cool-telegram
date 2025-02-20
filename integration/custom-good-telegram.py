#!/usr/bin/env python
# Script for creating Telegram messages out of Wazuh alert_json
# Config files are located on "/usr/share/wazuh-good-telegram"

import argparse
import json
import os
import re as _re
import sys
import time
import traceback

parser = argparse.ArgumentParser(
    description="Script for creating Telegram messages out of Wazuh Alerts"
)
parser.add_argument("alert_json")
parser.add_argument("api_token")
parser.add_argument("-l", "--log_path", help="set a different log path")
args = parser.parse_args()

pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TIMEOUT = 360
CONFIG_PATH = "/usr/share/wazuh-good-telegram"
LOG_PATH = args.log_path if args.log_path else f"{pwd}/logs/integrations.log"


class Templater:
    pat = r"\$\{(.*?)\}"
    pattern = _re.compile(pat)

    def __init__(self, parse_mode):
        self.parse_mode = parse_mode

        # Markdown escape regex based on https://github.com/python-telegram-bot/python-telegram-bot/blob/v21.10/telegram/helpers.py#L45-L78
        if self.parse_mode == "Markdown":
            escape_chars = r"_*`["
        elif self.parse_mode == "MarkdownV2":
            escape_chars = r"\_*[]~`>#+-=|.!"
        else:
            raise ValueError(
                "Parse mode node supported, set it to Markdown or MarkdownV2"
            )

        self.escape = _re.compile(f"([{_re.escape(escape_chars)}])")

    def substitute(self, template, mapping) -> str:
        """
        Replaces words surrounded by {} with their respective attributes in the mapping dict
        """

        # Helper function for .sub()
        def convert(mo):
            match = mo.group()[2:-1]
            split = match.split(".")
            if match is not None:
                cursor = mapping
                for key in split:
                    try:
                        cursor = cursor[key]
                    except KeyError:
                        return self.escape_markdown(mo.group())

                return self.escape_markdown(str(cursor))
            return self.escape_markdown(mo.group())

        return self.pattern.sub(convert, template)

    def escape_markdown(self, text):
        return self.escape.sub(r"\\\1", text)

    def escape_brackets(self, text):
        return _re.sub(f"([{_re.escape(r'{}()')}])", r"\\\1", text)


class Logger:
    def __init__(self, log_path):
        self.log_path = log_path

    def log(self, msg):
        """
        Writes message to log file
        """
        now = time.strftime("%a %b %d %H:%M:%S %Z %Y")

        msg = f"{now}| Custom-Good-Telegram | {msg} \n"
        print(msg, end="")

        with open(self.log_path, "a", encoding="utf-8") as file_io:
            file_io.write(msg)


def make_alert(alert_json):
    """
    Interprets the alert args and converts it into a POST request to Telegeram
    """

    logger.log("Parsing alert json")

    alert_id = str(alert_json["rule"]["id"])
    with open(f"{CONFIG_PATH}/config.yaml") as file_io:
        config = yaml.safe_load(file_io)

    templater = Templater(config["parse_mode"])
    chat_id = config["chat_id"]

    rule_id = config["rule_id"]["default"] | (
        config["rule_id"][alert_id] if alert_id in config["rule_id"] else {}
    )

    content = f"{templater.substitute(rule_id["message"], alert_json)}"

    message = {
        "chat_id": chat_id,
        "text": templater.escape_brackets(content),
        "parse_mode": config["parse_mode"],
    }

    logger.log("Parsing done")
    logger.log(f"Message: {message}")

    post_params = {
        "url": f"https://api.telegram.org/bot{args.api_token}/SendMessage",
        "headers": {"content-type": "application/json"},
        "data": json.dumps(message),
        "timeout": TIMEOUT,
    }
    response_action = requests.post(**post_params)

    logger.log(
        f"POST request done, response is: {response_action}\n {response_action.content}"
    )


logger = Logger(LOG_PATH)

try:
    import requests
    import yaml
except ImportError:
    pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    logger.log(
        "Missing modules.\nInstall: pip install requests\nInstall: pip install pyyaml",
    )
    sys.exit(1)

if not os.path.isfile(f"{CONFIG_PATH}/config.yaml"):
    logger.log(
        f"Missing config files on {CONFIG_PATH}",
    )
    sys.exit(1)


if __name__ == "__main__":
    try:
        logger.log("good-telegram started:")

        with open(args.alert_json, encoding="utf-8") as alert_file:
            alert_json = json.loads(alert_file.read())

        make_alert(alert_json)
    except Exception as _general_e:
        logger.log("".join(traceback.format_exception(_general_e)))
        raise _general_e
