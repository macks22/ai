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

OPS = set([
    Operation(
        'climb-on-chair',
        set((chair_at_middle_room, at_middle_room, on_floor)),
        set((at_bananas, on_chair)),
        set((at_middle_room, on_floor))
    ),
    Operation(
        'push-chair-from-door-to-middle-room',
        set((chair_at_door, at_door)),
        set((chair_at_middle_room, at_middle_room)),
        set((chair_at_door, at_door))
    ),
    Operation(
        'walk-from-door-to-middle-room',
        set((at_door, on_floor)),
        set((at_middle_room,)),
        set((at_door,))
    ),
    Operation(
        'grasp-bananas',
        set((at_bananas, empty_handed)),
        set((has_bananas,)),
        set((empty_handed,))
    ),
    Operation(
        'drop-ball',
        set((has_ball,)),
        set((empty_handed,)),
        set((has_ball,))
    ),
    Operation(
        'eat-bananas',
        set((has_bananas,)),
        set((empty_handed, not_hungry)),
        set((has_bananas, hungry))
    )
])

# =============================================================================
# PROBLEM
# =============================================================================

GOAL = set((not_hungry,))

STATE = set((at_door, on_floor, has_ball, hungry, chair_at_door))

PROBLEM = Problem(GOAL, STATE, OPS)
