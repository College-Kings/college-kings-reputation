from enum import Enum
import enum

"""renpy
init python:
"""


class RepComponent(Enum):
    BRO = enum.auto()
    BOYFRIEND = enum.auto()
    TROUBLEMAKER = enum.auto()

    @classmethod
    def _missing_(cls, value: object) -> "RepComponent":
        return cls.BRO
