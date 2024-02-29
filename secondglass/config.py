import os
from configparser import ConfigParser
from typing import Any, Mapping

APP_NAME = "secondglass"
VERSION = 2

DEFAULT_SETTINGS: Mapping[str, Mapping[str, Any]] = {
    "CONFIG_VERSION": {
        "config_version": VERSION,
    },
    "STATIC": {  # can't be changed from UI
        "font_init_size": 18,
        "font_family": "Calibri Light",
        "render_delay_ms": 30,
        "wh_ratio_threshold": 2.6,
    },
    "DYNAMIC": {  # can be changed from UI
        "init_text_input": "5 minutes",
        "sound": "hit",
        "ui_theme": "darkly",  # litera cosmo cerculean /  superhero darkly
        "prevent_screensaver": False,
    },
    "AUDIOFILES": {
        "wood": "185846__lloydevans09__light-wood.wav",
        "hit": "186401__lloydevans09__balsa-hit-1.wav",
        "spin": "186993__lloydevans09__wood-spin.wav",
        "rattle": "332001__lloydevans09__spray_can_rattle.wav",
        "ding": "338148__artordie__ding.wav",
        "metalic": "464420__michael_grinnell__metalic_ching_keys_2.wav",
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


def _update_config_version(config: ConfigParser, path: str) -> ConfigParser:
    if (
        config.getint("CONFIG_VERSION", "config_version", fallback=0)
        == VERSION
    ):
        return config
    new_config = ConfigParser()
    new_config.read_dict(DEFAULT_SETTINGS)
    for section in config:
        if section not in new_config:
            continue
        for name in config[section]:
            if name not in new_config[section]:
                continue
            new_config[section][name] = config[section][name]
    save_settings(new_config)
    return new_config


CONFIG_PATH = _get_conf_path()


def save_settings(config: ConfigParser) -> None:
    with open(CONFIG_PATH, "w") as configfile:
        config.write(configfile)


def _get_config() -> ConfigParser:
    config = ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        config.read_dict(DEFAULT_SETTINGS)
        save_settings(config)
    config.read(CONFIG_PATH)

    return _update_config_version(config, CONFIG_PATH)


SETTINGS = _get_config()

__all__ = ["SETTINGS", "save_settings"]
