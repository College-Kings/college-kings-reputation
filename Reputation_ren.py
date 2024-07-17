from typing import Optional, Union
from game.characters.NonPlayableCharacter_ren import NonPlayableCharacter
from game.reputation.ReputationService_ren import ReputationService

from game.reputation.RepComponent_ren import RepComponent
from game.reputation.Reputations_ren import Reputations
import renpy.exports as renpy

locked_reputation: bool
pb_reputation_notification: bool
_in_replay: bool

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

    def __call__(
        self, npc: Optional[NonPlayableCharacter] = None
    ) -> Union["Reputations", bool]:
        if npc is None:
            return self._get_reputation()
        else:
            return self._npc_rep_check(npc)

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

    @property
    def popular(self) -> bool:
        return self() == Reputations.POPULAR

    @property
    def confident(self) -> bool:
        return self() == Reputations.CONFIDENT

    @property
    def loyal(self) -> bool:
        return self() == Reputations.LOYAL

    def _get_reputation(self) -> "Reputations":
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

    def _npc_rep_check(self, npc: NonPlayableCharacter) -> bool:
        return self._get_reputation() == npc.preferred_reputation

    def add_point(
        self, var: Union[RepComponent, NonPlayableCharacter], value: int = 1
    ) -> None:
        # Don't update reputation if reputation is locked
        if locked_reputation or _in_replay:
            return

        old_reputation = self()
        assert isinstance(old_reputation, Reputations)

        if isinstance(var, RepComponent):
            self._add_points_by_component(var, value)
        else:
            self._add_point_by_npc(var, value)

        new_reputation = self()
        assert isinstance(new_reputation, Reputations)

        # Notify user on reputation change
        if new_reputation != old_reputation:
            renpy.notify(f"Your reputation has changed to {new_reputation.name}")

    def _add_point_by_npc(self, npc: NonPlayableCharacter, value: int) -> None:
        return None
        # target_rep = npc.preferred_reputation

        # if target_rep == Reputations.POPULAR:

        #     component = sorted()

        # points_to_popular = {
        #     RepComponent.BRO: reputation.components[RepComponent.BOYFRIEND]
        #     - reputation.components[RepComponent.BRO],
        #     RepComponent.TROUBLEMAKER: reputation.components[RepComponent.BOYFRIEND]
        #     - reputation.components[RepComponent.TROUBLEMAKER],
        # }
        # points_to_loyal = {
        #     RepComponent.BRO: reputation.components[RepComponent.TROUBLEMAKER]
        #     - reputation.components[RepComponent.BRO],
        #     RepComponent.BOYFRIEND: reputation.components[RepComponent.TROUBLEMAKER]
        #     - reputation.components[RepComponent.BOYFRIEND],
        # }
        # points_to_confident = {
        #     RepComponent.BOYFRIEND: reputation.components[RepComponent.BRO]
        #     - reputation.components[RepComponent.BOYFRIEND],
        #     RepComponent.TROUBLEMAKER: reputation.components[RepComponent.BRO]
        #     - reputation.components[RepComponent.TROUBLEMAKER],
        # }

        # self._add_points_by_component(component, value)

    def _add_points_by_component(self, component: RepComponent, value: int) -> None:
        if pb_reputation_notification:
            renpy.notify(f"{component.name.capitalize()} point added")

        self.components[component] += value

    def change_reputation(self, target_reputation: "Reputations") -> None:
        ReputationService.change_reputation(self, target_reputation)

    def is_popular(self) -> bool:
        return self() == Reputations.POPULAR

    def is_confident(self) -> bool:
        return self() == Reputations.CONFIDENT

    def is_loyal(self) -> bool:
        return self() == Reputations.LOYAL
