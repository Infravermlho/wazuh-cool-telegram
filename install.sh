#!/bin/bash
set -e

SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "${SCRIPT_PATH}")
CONFIG_PATH="/usr/share/wazuh-good-telegram"

cd "${SCRIPT_DIR}" || return

echo -e "Moving the integration to /var/ossec/integrations/"
mkdir -p "/var/ossec/integrations/" && cp "${SCRIPT_DIR}/integration/custom-good-telegram.py" "/var/ossec/integrations/custom-good-telegram.py"
chmod 750 /var/ossec/integrations/custom-good-telegram.py
chown root:wazuh /var/ossec/integrations/custom-good-telegram.py | echo -e "Wazuh user not found"

if [ -e ${CONFIG_PATH} ]; then
  echo -e "Config files found, overwrite? (y/n)"
  read -s -r -n 1 key

  if [ "$key" = "y" ]; then
    mkdir -p "${CONFIG_PATH}" && cp "${SCRIPT_DIR}/default.config.yaml" "${CONFIG_PATH}/config.yaml"
  fi
else
  echo -e "config files not found, creating"
  mkdir -p "${CONFIG_PATH}" && cp "${SCRIPT_DIR}/default.config.yaml" "${CONFIG_PATH}/config.yaml"
fi

cp "${SCRIPT_DIR}/default.config.yaml" "${CONFIG_PATH}/default.config.yaml"
echo -e "custom-good-telegram installed sucessfully"
