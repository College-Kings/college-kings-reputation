from typing import Union
from game.reputation.ReputationService_ren import ReputationService

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

    def __call__(self) -> "Reputations":
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
            old_components = self.__dict__.get("components", {})
            self._components = {k: v for k, v in old_components.items()}

        try:
            self._components
        except AttributeError:
            self._components = {}

        old: dict[Union[RepComponent, Reputations, str], int] = {
            k: v for k, v in self._components.items()
        }
        for k, v in old.items():
            if k == "bro" or k == Reputations.BRO:
                self._components[RepComponent.BRO] = v
            elif k == "boyfriend" or k == Reputations.BOYFRIEND:
                self._components[RepComponent.BOYFRIEND] = v
            elif k == "troublemaker" or k == Reputations.TROUBLEMAKER:
                self._components[RepComponent.TROUBLEMAKER] = v

        return self._components

    @components.setter
    def components(self, value: dict[RepComponent, int]) -> None:
        self._components = value

    @property
    def sorted_reputations(self) -> list["Reputations"]:
        return ReputationService.sort_reputation(self.components)

    def add_point(self, var: RepComponent, value: int = 1) -> None:
        ReputationService.add_points(self, var, value)

    def change_reputation(self, target_reputation: "Reputations") -> None:
        ReputationService.change_reputation(self, target_reputation)

    def is_popular(self) -> bool:
        return self() == Reputations.POPULAR

    def is_confident(self) -> bool:
        return self() == Reputations.CONFIDENT

    def is_loyal(self) -> bool:
        return self() == Reputations.LOYAL
