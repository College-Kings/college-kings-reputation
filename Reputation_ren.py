"""renpy
init python:
"""

from game.reputation.RepComponent_ren import RepComponent
from game.reputation.Reputations_ren import Reputations


class Reputation:
    def __init__(self):
        self.components = {
            RepComponent.BRO: 1,
            RepComponent.BOYFRIEND: 2,
            RepComponent.TROUBLEMAKER: 2,
        }

    def __call__(self):
        bro = self.components[RepComponent.BRO]
        boyfriend = self.components[RepComponent.BOYFRIEND]
        troublemaker = self.components[RepComponent.TROUBLEMAKER]

        # Sort reputation values
        reputation_dict = {
            Reputations.POPULAR: bro * troublemaker / float(boyfriend),
            Reputations.CONFIDENT: boyfriend * troublemaker / float(bro),
            Reputations.LOYAL: bro * boyfriend / float(troublemaker),
        }

        return max(reputation_dict, key=lambda k: reputation_dict[k])

    @property
    def sorted_reputations(self):
        bro = self.components[RepComponent.BRO]
        boyfriend = self.components[RepComponent.BOYFRIEND]
        troublemaker = self.components[RepComponent.TROUBLEMAKER]

        # Sort reputation values
        reputation_dict = {
            Reputations.POPULAR: bro * troublemaker / float(boyfriend),
            Reputations.CONFIDENT: boyfriend * troublemaker / float(bro),
            Reputations.LOYAL: bro * boyfriend / float(troublemaker),
        }

        return [
            k
            for k, v in sorted(
                reputation_dict.items(), key=helper_sorted_by_value, reverse=True
            )
        ]

    def add_point(self, var: Reputations, value: int = 1):
        # Don't update reputation if reputation is locked
        if locked_reputation or _in_replay:
            return

        if pb_reputation_notification:
            renpy.show_screen("popup", message=f"{var.name.capitalize()} point added")

        old_reputation = self()

        self.components[var] += value

        # Notify user on reputation change
        if self() != old_reputation:
            renpy.notify(f"Your reputation has changed to {self().name}")

    def change_reputation(self, target_reputation: Reputations):
        if not config.developer:
            print("Debug functions are only available in the development enviroment.")
            return

        if target_reputation == Reputations.POPULAR:
            self.components = {
                RepComponent.BRO: 999,
                RepComponent.TROUBLEMAKER: 999,
                RepComponent.BOYFRIEND: 1,
            }

        elif target_reputation == Reputations.LOYAL:
            self.components = {
                RepComponent.BRO: 999,
                RepComponent.TROUBLEMAKER: 1,
                RepComponent.BOYFRIEND: 999,
            }

        elif target_reputation == Reputations.CONFIDENT:
            self.components = {
                RepComponent.BRO: 1,
                RepComponent.TROUBLEMAKER: 999,
                RepComponent.BOYFRIEND: 999,
            }


def helper_sorted_by_value(item):
    return item[1]
