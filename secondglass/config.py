import os
from configparser import ConfigParser
from typing import Any, Mapping

APP_NAME = "secondglass"

default_settings: Mapping[str, Mapping[str, Any]] = {
    "STATIC": {
        "ui_theme": "darkly",  # litera cosmo cerculean /  superhero darkly
        "font_init_size": 18,
        "font_family": "Calibri Light",
        "render_delay_ms": 30,
        "wh_ratio_threshold": 2.6,
    },
    "DYNAMIC": {
        "init_text_input": "5 minutes",
    },
}
CONF_DIR_NAME = APP_NAME
CONF_FILE_NAME = f"{APP_NAME}_settings.ini"


def _get_conf_path() -> str:
    if os.path.isfile(CONF_FILE_NAME):  # located in the same directory
        return CONF_FILE_NAME

    default_config_path = None
    if "APPDATA" in os.environ:  # windows
        default_config_path = os.environ["APPDATA"]
    elif "XDG_CONFIG_HOME" in os.environ:  # linux
        default_config_path = os.environ["XDG_CONFIG_HOME"]
    else:
        return CONF_FILE_NAME

    config_dir_path = os.path.join(default_config_path, CONF_DIR_NAME)
    if not os.path.isdir(config_dir_path):
        os.mkdir(config_dir_path)

    config_path = os.path.join(config_dir_path, CONF_FILE_NAME)
    return config_path


CONFIG_PATH = _get_conf_path()


def save_settings(config: ConfigParser) -> None:
    with open(CONFIG_PATH, "w") as configfile:
        config.write(configfile)


def _get_config() -> ConfigParser:
    config = ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        config.read_dict(default_settings)
        save_settings(config)
    config.read(CONFIG_PATH)
    return config


SETTINGS = _get_config()
