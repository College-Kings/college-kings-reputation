import renpy.exports as renpy

from game.reputation.RepComponent_ren import RepComponent
from game.reputation.Reputations_ren import Reputations

locked_reputation: bool
_in_replay: bool
pb_reputation_notification: bool

"""renpy
init python:
"""


class Reputation:
    def __init__(self) -> None:
        self._components: dict[RepComponent, int] = {
            RepComponent.BRO: 1,
            RepComponent.BOYFRIEND: 2,
            RepComponent.TROUBLEMAKER: 2,
        }

    def __call__(self) -> Reputations:
        bro: int = self.components[RepComponent.BRO]
        boyfriend: int = self.components[RepComponent.BOYFRIEND]
        troublemaker: int = self.components[RepComponent.TROUBLEMAKER]

        # Sort reputation values
        reputation_dict: dict[Reputations, float] = {
            Reputations.POPULAR: bro * troublemaker / float(boyfriend),
            Reputations.CONFIDENT: boyfriend * troublemaker / float(bro),
            Reputations.LOYAL: bro * boyfriend / float(troublemaker),
        }

        return max(reputation_dict, key=lambda k: reputation_dict[k])

    @property
    def components(self) -> dict[RepComponent, int]:
        try:
            self._components
        except AttributeError:
            if self.__dict__.get("components", {}):
                self._components = {
                    k: v for k, v in self.__dict__["components"].items()
                }

        old = {k: v for k, v in self._components.items()}
        for k, v in old.items():
            if k == "bro" or k == Reputations.BRO:  # type: ignore
                self._components[RepComponent.BRO] = v
            elif k == "boyfriend" or k == Reputations.BOYFRIEND:  # type: ignore
                self._components[RepComponent.BOYFRIEND] = v
            elif k == "troublemaker" or k == Reputations.TROUBLEMAKER:  # type: ignore
                self._components[RepComponent.TROUBLEMAKER] = v

        return self._components

    @components.setter
    def components(self, value: dict[RepComponent, int]) -> None:
        self._components = value

    @property
    def sorted_reputations(self) -> list[Reputations]:
        bro: int = self.components[RepComponent.BRO]
        boyfriend: int = self.components[RepComponent.BOYFRIEND]
        troublemaker: int = self.components[RepComponent.TROUBLEMAKER]

        # Sort reputation values
        reputation_dict: dict[Reputations, float] = {
            Reputations.POPULAR: bro * troublemaker / float(boyfriend),
            Reputations.CONFIDENT: boyfriend * troublemaker / float(bro),
            Reputations.LOYAL: bro * boyfriend / float(troublemaker),
        }

        return [
            k
            for k, _ in sorted(
                reputation_dict.items(), key=helper_sorted_by_value, reverse=True
            )
        ]

    def add_point(self, var: RepComponent, value: int = 1) -> None:
        # Don't update reputation if reputation is locked
        if locked_reputation or _in_replay:
            return

        if pb_reputation_notification:
            renpy.notify(f"{var.name.capitalize()} point added")

        old_reputation: Reputations = self()

        self.components[var] += value

        # Notify user on reputation change
        if self() != old_reputation:
            renpy.notify(f"Your reputation has changed to {self().name}")

    def change_reputation(self, target_reputation: Reputations) -> None:
        if target_reputation == Reputations.POPULAR:
            self.components = {
                RepComponent.BRO: 20,
                RepComponent.TROUBLEMAKER: 20,
                RepComponent.BOYFRIEND: 10,
            }

        elif target_reputation == Reputations.LOYAL:
            self.components = {
                RepComponent.BRO: 20,
                RepComponent.TROUBLEMAKER: 10,
                RepComponent.BOYFRIEND: 20,
            }

        elif target_reputation == Reputations.CONFIDENT:
            self.components = {
                RepComponent.BRO: 10,
                RepComponent.TROUBLEMAKER: 20,
                RepComponent.BOYFRIEND: 20,
            }


def helper_sorted_by_value(item: tuple[object, float]) -> float:
    return item[1]
