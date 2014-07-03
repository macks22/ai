"""
The knowledge domain for the "Monkey and Bananas" problem.

"""
from gps import Condition, Operation, Problem


# =============================================================================
# CONDITIONS
# =============================================================================

chair_at_middle_room = Condition('chair-at-middle-room')
at_middle_room = Condition('at-middle-room')
on_floor = Condition('on-floor')
on_chair = Condition('on-chair')
at_bananas = Condition('at-bananas')
chair_at_door = Condition('chair-at-door')
at_door = Condition('at-door')
empty_handed = Condition('empty-handed')
has_bananas = Condition('has-bananas')
has_ball = Condition('has-ball')
not_hungry = Condition('not-hungry')
hungry = Condition('hungry')

# =============================================================================
# OPERATIONS
# =============================================================================

OPS = (
    Operation(
        'climb-on-chair',
        (chair_at_middle_room, at_middle_room, on_floor),
        (at_bananas, on_chair),
        (at_middle_room, on_floor)
    ),
    Operation(
        'push-chair-from-door-to-middle-room',
        (chair_at_door, at_door),
        (chair_at_middle_room, at_middle_room),
        (chair_at_door, at_door)
    ),
    Operation(
        'walk-from-door-to-middle-room',
        (at_door, on_floor),
        (at_middle_room,),
        (at_door,)
    ),
    Operation(
        'grasp-bananas',
        (at_bananas, empty_handed),
        (has_bananas,),
        (empty_handed,)
    ),
    Operation(
        'drop-ball',
        (has_ball,),
        (empty_handed,),
        (has_ball,)
    ),
    Operation(
        'eat-bananas',
        (has_bananas,),
        (empty_handed, not_hungry),
        (has_bananas, hungry)
    )
)

# =============================================================================
# PROBLEM
# =============================================================================

GOAL = (not_hungry,)

STATE = (at_door, on_floor, has_ball, hungry, chair_at_door)

PROBLEM = Problem(GOAL, STATE, OPS)
