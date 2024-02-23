from os.path import isfile

from pygame import mixer

from secondglass.config import SETTINGS
from secondglass.helpers import pyinstaller_fix_path

mixer.init()


def get_beep_file_path(sound_name: str | None = None) -> str:
    name = sound_name or SETTINGS["DYNAMIC"]["sound"]
    file_name = SETTINGS["AUDIOFILES"][name]
    if isfile(file_name):
        return file_name
    return pyinstaller_fix_path("resources/sounds/" + file_name)


_sound = mixer.Sound(get_beep_file_path())


def play_beep(update: bool = False) -> None:
    global _sound

    if update:
        _sound = mixer.Sound(get_beep_file_path())
    _sound.play()
