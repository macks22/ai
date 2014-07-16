"""
The knowledge domain for the "Driving to School" problem.

"""
from problem import Condition, Operation, Problem


# =============================================================================
# CONDITIONS
# =============================================================================

son_at_home = Condition('son-at-home')
car_works = Condition('car-works')
son_at_school = Condition('son-at-school')
car_needs_battery = Condition('car-needs-battery')
shop_knows_problem = Condition('shop-knows-problem')
shop_has_money = Condition('shop-has-money')
in_communication_with_shop = Condition('in-communication-with-shop')
have_phone_book = Condition('have-phone-book')
know_phone_number = Condition('know-phone-number')
have_money = Condition('have-money')

# =============================================================================
# OPERATIONS
# =============================================================================

_OPS = (
    Operation(
        'drive-son-to-school',
        (son_at_home, car_works),
        (son_at_school,),
        (son_at_home,)
    ),
    Operation(
        'shop-installs-battery',
        (car_needs_battery, shop_knows_problem, shop_has_money),
        (car_works,)
    ),
    Operation(
        'tell-shop-problem',
        (in_communication_with_shop,),
        (shop_knows_problem,)
    ),
    Operation(
        'telephone-shop',
        (know_phone_number,),
        (in_communication_with_shop,)
    ),
    Operation(
        'look-up-number',
        (have_phone_book,),
        (know_phone_number,)
    ),
    Operation(
        'give-shop-money',
        (have_money,),
        (shop_has_money,),
        (have_money,)
    )
)

# =============================================================================
# PROBLEM
# =============================================================================

_GOAL = (son_at_school,)

_STATE = (son_at_home, car_needs_battery, have_money, have_phone_book)

PROBLEM = Problem(_GOAL, _STATE, _OPS, 'drive-son-to-school')

# =============================================================================
# PROBLEMS THAT EXPOSE LIMITATIONS OF V1
# =============================================================================

LBYL_PROBLEM = Problem((son_at_school, have_money), _STATE, _OPS,
    'look-before-you-leap')

CLOBBERING_PROBLEM = Problem((have_money, son_at_school), _STATE, _OPS,
    'prerequisite-clobbers-sibling-goal')

"""
Danger of infinite oscillation between 'get-phone-number' and 'call-shop'.

"""
_RECURSIVE_OPS = (
    Operation(
        'tell-shop-problem',
        preconditions=(in_communication_with_shop,),
        add_list=(shop_knows_problem,)
    ),
    Operation(
        'get-phone-number',
        preconditions=(in_communication_with_shop,),
        add_list=(know_phone_number,)
    ),
    Operation(
        'call-shop',
        preconditions=(know_phone_number,),
        add_list=(in_communication_with_shop,)
    )
)

RECURSIVE_SUBGOAL_PROBLEM = Problem((shop_knows_problem,), (), _RECURSIVE_OPS,
    'recursive-subgoal')
