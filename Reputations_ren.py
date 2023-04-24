from __future__ import annotations
from enum import Enum
import enum


"""renpy
init python:
"""


class Reputations(Enum):
    POPULAR = enum.auto()
    CONFIDENT = enum.auto()
    LOYAL = enum.auto()

    BRO = "bro"
    BOYFRIEND = "boyfriend"
    TROUBLEMAKER = "troublemaker"

    @classmethod
    def _missing_(cls, value) -> Reputations:
        return cls.POPULAR
