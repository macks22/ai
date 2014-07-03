"""
An object-oriented General Problem Solver (GPS) implementation.
Adapted from ch. 4 of Peter Norvig's "Paradigms of Artificial Intelligence
Programming."

"""


class Condition(object):
    """Represent a condition: some information about the world."""

    def __init__(self, name):
        """
        :param str name: The unique name of the condition.

        """
        self.name = name

    def __eq__(self, other_condition):
        return self.name == other_condition.name

    def __repr__(self):
        return self.name.upper()

    def __str__(self):
        return repr(self)


class Problem(object):
    """A problem which can be solved by the GPS."""

    def __init__(self, goal, state, ops):
        """
        :type  goal: set of :class:Condition
        :param goal: The set of Conditions we need to achieve in order to say
            that we have solved this problem.
        :type  state: set of :class:Condition
        :param state: The set of conditions that currently stand.
        :type  ops: set of :class:Operation
        :param ops: The set of allowable operations we can apply in order to
            achieve our goal conditions.

        """
        self.goal = goal
        self.state = state
        self.ops = ops

    def __repr__(self):
        rep = ['Goal:']
        rep += ['    {}'.format(cond) for cond in self.goal]
        rep.append('\nState:')
        rep += ['    {}'.format(cond) for cond in self.state]
        rep.append('\nAllowable Operations:')
        rep += ['    {}'.format(op) for op in self.ops]
        return '\n'.join(rep)

    def __str__(self):
        return repr(self)


class Operation(object):
    """Some means to an end (goal)."""

    def __init__(self, action, preconditions, add_list, del_list=None):
        """
        :param str action: The action performed by this operation.
        :type  preconditions: set of :class:Condition
        :param preconditions: Set of conditions which must be true in order to
            apply this operation.
        :type  add_list: set of :class:Condition
        :param add_list: Set of the conditions that will be added to the
            current state when this operation is applied.
        :type  del_list: set of :class:Condition
        :param del_list: Set of the conditions that will be deleted from the
            current state when this operation is applied.

        """
        self.action = action
        self.preconditions = set() if preconditions is None else preconditions
        self.add_list = set() if add_list is None else add_list
        self.del_list = set() if del_list is None else del_list

    def __repr__(self):
        return self.action.upper()

    def __str__(self):
        return repr(self)


class GPS(object):
    """The general problem solver."""

    def solve(self, problem):
        """Solve a particular problem using means-ends analysis.

        :type  problem: :class:Problem
        :param problem: The problem to solve.

        """
        self.state = problem.state
        self.ops = problem.ops
        return self.achieve_all(problem.goal)

    def achieve_all(self, conds):
        """Attempt to achieve each condition in the set of conditions.

        :param set conds: The set of conditions to attempt to achieve.
        :rtype:  str or None
        :return: "SUCCESS" if the problem is solved, else None.

        """
        for cond in conds:
            status = self.achieve(cond)
            if not status:
                return None

        return "SUCCESS"

    def achieve(self, cond):
        """Attempt to achieve a particular condition.

        :type  cond: :class:Condition
        :param cond: The condition that we are attempting to achieve.
        :rtype:  bool
        :return: True if the condition was achieved, else False.

        """
        # case 1: base case (condition is in current state)
        if cond in self.state:
            return True

        # case 2: there exists some set of operations to put the condition in
        # the current state
        for op in self.ops:
            if self.is_appropriate(op, cond):
                self.apply_op(op)
                return True

        return False


    def apply_op(self, op):
        """Apply a particular operation by adding all conditions in its
        add-list and removing all in its delete-list.

        :type  op: :class:Operation
        :param op: The operation to apply.

        """
        if (all(map(self.achieve, op.preconditions))):
            print 'Executing ' + op.action
            self.state.difference_update(op.del_list)
            self.state.union(op.add_list)

    def is_appropriate(self, op, goal):
        """Evaluate if a particular operation is appropriate for solving some
        goal.

        :type  op: :class:Operation
        :param op: The operation to apply.
        :type  goal: :class:Condition
        :param goal: The goal we are trying to achieve by applying the op.
        :rtype:  bool
        :return: True if the op is appropriate, else False.

        """
        return goal in op.add_list
