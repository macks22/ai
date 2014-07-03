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

OPS = [
    Operation(
        'drive-son-to-school',
        set((son_at_home, car_works)),
        set((son_at_school,)),
        set((son_at_home,))
    ),
    Operation(
        'shop-installs-battery',
        set((car_needs_battery, shop_knows_problem, shop_has_money)),
        set((car_works,))
    ),
    Operation(
        'tell-shop-problem',
        set((in_communication_with_shop,)),
        set((shop_knows_problem,))
    ),
    Operation(
        'telephone-shop',
        set((know_phone_number,)),
        set((in_communication_with_shop,))
    ),
    Operation(
        'look-up-number',
        set((have_phone_book,)),
        set((know_phone_number,))
    ),
    Operation(
        'give-shop-money',
        set((have_money,)),
        set((shop_has_money,)),
        set((have_money,))
    )
]

# =============================================================================
# PROBLEM
# =============================================================================

GOAL = set((son_at_school,))

STATE = set((son_at_home, car_needs_battery, have_money, have_phone_book))

PROBLEM = Problem(GOAL, STATE, OPS)
