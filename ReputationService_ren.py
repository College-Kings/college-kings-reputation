from game.reputation.RepComponent_ren import RepComponent
from game.reputation.Reputation_ren import Reputation
from game.reputation.Reputations_ren import Reputations

locked_reputation: bool
pb_reputation_notification: bool

"""renpy
init python:
"""


class ReputationService:
    @staticmethod
    def sort_reputation(components: dict[RepComponent, int]) -> list["Reputations"]:
        bro: int = components[RepComponent.BRO]
        boyfriend: int = components[RepComponent.BOYFRIEND]
        troublemaker: int = components[RepComponent.TROUBLEMAKER]

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

    @staticmethod
    def change_reputation(
        reputation: Reputation, target_reputation: "Reputations"
    ) -> None:
        if target_reputation == Reputations.POPULAR:
            reputation.components = {
                RepComponent.BRO: 20,
                RepComponent.TROUBLEMAKER: 20,
                RepComponent.BOYFRIEND: 10,
            }

        elif target_reputation == Reputations.LOYAL:
            reputation.components = {
                RepComponent.BRO: 20,
                RepComponent.TROUBLEMAKER: 10,
                RepComponent.BOYFRIEND: 20,
            }

        elif target_reputation == Reputations.CONFIDENT:
            reputation.components = {
                RepComponent.BRO: 10,
                RepComponent.TROUBLEMAKER: 20,
                RepComponent.BOYFRIEND: 20,
            }


def helper_sorted_by_value(item: tuple[object, float]) -> float:
    return item[1]
