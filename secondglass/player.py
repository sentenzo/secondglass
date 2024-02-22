from os.path import isfile

import pyglet

from secondglass.config import SETTINGS
from secondglass.helpers import pyinstaller_fix_path


def get_beep_file_path(sound_name: str | None = None) -> str:
    name = sound_name or SETTINGS["DYNAMIC"]["sound"]
    file_name = SETTINGS["AUDIOFILES"][name]
    if isfile(file_name):
        return file_name
    return pyinstaller_fix_path("resources/sounds/" + file_name)


def play_beep(sound_name: str | None = None) -> None:
    source = pyglet.media.load(get_beep_file_path(sound_name))
    source.play()


"""

from pygame import mixer

from secondglass.helpers import pyinstaller_fix_path

FILE_NAME = "186401__lloydevans09__balsa-hit-1.wav"

BEEP_FILE_LOCATION = pyinstaller_fix_path(
    "resources/sounds/" + FILE_NAME
)
mixer.init()

SOUND = mixer.Sound(BEEP_FILE_LOCATION)


def play_beep() -> None:
    SOUND.play()

"""
