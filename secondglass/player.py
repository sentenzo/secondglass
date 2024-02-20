import pyglet
from pyglet.media.codecs import Source

from secondglass.helpers import pyinstaller_fix_path

FILE_NAME = "186401__lloydevans09__balsa-hit-1.wav"

BEEP_FILE_LOCATION = pyinstaller_fix_path("resources/sounds/" + FILE_NAME)

_cur_source: Source = pyglet.media.load(BEEP_FILE_LOCATION)


def play_beep() -> None:
    global _cur_source
    _cur_source.play()
    _cur_source = pyglet.media.load(BEEP_FILE_LOCATION)


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
