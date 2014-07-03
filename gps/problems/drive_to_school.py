"""
The knowledge domain for the "Driving to School" problem.

"""
from gps import Condition, Operation, Problem


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

OPS = (
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

GOAL = (son_at_school,)

STATE = (son_at_home, car_needs_battery, have_money, have_phone_book)

PROBLEM = Problem(GOAL, STATE, OPS)
