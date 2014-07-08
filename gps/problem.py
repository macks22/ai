"""
This module contains the necessary classes for formulating a problem for the
general problem solver (GPS) implemented in gps.py. In particular, a problem is
composed of:

1.  A goal: a set of Condition objects
2.  A starting state: a set of Condition objects
3.  Allowable operations: a set of Operation objects

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

    def __init__(self, goal, state, ops, name='unnamed'):
        """
        :type  goal: ordered collection of :class:Condition
        :param goal: The set of Conditions we need to achieve in order to say
            that we have solved this problem.
        :type  state: collection of :class:Condition
        :param state: The set of conditions that currently stand.
        :type  ops: collection of :class:Operation
        :param ops: The set of allowable operations we can apply in order to
            achieve our goal conditions.

        """
        self.goal = goal
        self.state = set(state)
        self.ops = set(ops)
        self.name = name

    def __repr__(self):
        header = '{} PROBLEM'.format(self.name.upper())
        rep = [header, '-' * len(header)]
        rep.append('\nGoal:')
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

    def __init__(self, action, preconditions=(), add_list=(), del_list=()):
        """
        :param str action: The action performed by this operation.
        :type  preconditions: collection of :class:Condition
        :param preconditions: Set of conditions which must be true in order to
            apply this operation.
        :type  add_list: collection of :class:Condition
        :param add_list: Set of the conditions that will be added to the
            current state when this operation is applied.
        :type  del_list: collection of :class:Condition
        :param del_list: Set of the conditions that will be deleted from the
            current state when this operation is applied.

        """
        self.action = action
        self.preconditions = set(preconditions)
        self.add_list = set(add_list)
        self.del_list = set(del_list)

    def __repr__(self):
        return self.action.upper()

    def __str__(self):
        return repr(self)

    def simulate(self, state):
        """Simulate an execution of the operation. In other words, apply the
        operation to the state of the executor but don't actually perform the
        action that 'executes' this operation.

        :type  state: set of :class:Condition
        :param state: The state to apply the operation to.

        """
        self._apply(state)

    def execute(self, state):
        """Perform some action that 'executes' this operation. The default
        action simply prints 'Executing <action_name>'. This can be overriden to
        execute some callback or perform some set of operations. The execution
        of an operation will alter the state of the executor.

        :type  state: set of :class:Condition
        :param state: The state to apply the operation to.

        """
        print 'Executing {}'.format(self.action)
        self._apply(state)

    def _apply(self, state):
        """Apply the operation by adding all conditions in its add-list
        and removing all in its delete-list.

        """
        state.difference_update(self.del_list)
        state.union(self.add_list)
