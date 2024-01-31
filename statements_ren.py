from typing import Optional

from renpy.ast import PyExpr
from renpy.lexer import Lexer
import renpy.exports as renpy

from game.reputation.RepComponent_ren import RepComponent
from game.reputation.Reputation_ren import Reputation
from game.reputation.ReputationService_ren import ReputationService

locked_reputation: bool
pb_reputation_notification: bool
reputation = Reputation()

"""renpy
python early:
"""


def parse_add_rep_point(lexer: "Lexer") -> "PyExpr":
    rep_component: Optional[PyExpr] = lexer.simple_expression()
    if not rep_component:
        renpy.error("Expected RepComponent")

    return rep_component


def lint_add_rep_point(rep_component_expr: "PyExpr") -> None:
    try:
        eval(rep_component_expr)
    except Exception:
        renpy.error(f"Invalid achievement: {rep_component_expr}")


def execute_add_rep_point(rep_component_expr: "PyExpr") -> None:
    rep_component: RepComponent = eval(rep_component_expr)

    ReputationService.add_points(reputation, rep_component)


renpy.register_statement(
    name="add_rep_point",
    parse=parse_add_rep_point,
    lint=lint_add_rep_point,
    execute=execute_add_rep_point,
)
