"""
An object-oriented General Problem Solver (GPS) implementation.
Adapted from ch. 4 of Peter Norvig's "Paradigms of Artificial Intelligence
Programming."

"""


class GPS(object):
    """The general problem solver."""

    version = 1

    def solve(self, problem):
        """Solve a particular problem using means-ends analysis.

        :type  problem: :class:Problem
        :param problem: The problem to solve.

        """
        self.state = problem.state.copy()
        self.ops = problem.ops.copy()
        return self.achieve_all(problem.goal)

    def achieve_all(self, goals):
        """Attempt to achieve each goal in the set of goals.

        :param set goals: The set of goals to attempt to achieve.
        :rtype:  str or None
        :return: "SUCCESS" if the problem is solved, else None.

        """
        for goal in goals:
            status = self.achieve(goal)
            if not status:
                return None

        return "SUCCESS"

    def achieve(self, cond):
        """Attempt to achieve a particular goal.

        :type  cond: :class:Condition
        :param cond: The goal that we are attempting to achieve.
        :rtype:  bool
        :return: True if the goal was achieved, else False.

        """
        # case 1: base case (goal is in current state)
        if cond in self.state:
            return True

        # case 2: there exists some set of operations to put the goal in
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
            op.execute(self.state)

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


class GPSv2(GPS):
    """The second version of the general problem solver."""

    version = 2

    def __init__(self):
        self.reset()

    def solve(self, problem):
        """Solve a particular problem using means-ends analysis.

        :type  problem: :class:Problem
        :param problem: The problem to solve.

        """
        self.reset()
        self.state = problem.state.copy()
        self.ops = problem.ops.copy()
        self.goals = tuple(problem.goals)
        self.local_state = problem.state.copy()

        # we want to represent local states: one for each goal
        # let's use a dictionary because we'll also need a sequence of
        # operations for each goal (how to achieve it).
        for goal in problem.goals:
            self.solution_history[goal] = {'state': None, 'ops': None}

        return self.achieve_all()

    def reset(self):
        """Reset all local state variables to prepare for a new problem. These
        are kept around between problems in case one might want to inspect them.
        This is called at the beginning of a call to 'solve'.

        """
        self.local_state = None
        self.local_ops = []
        self.solution_history = {}
        self.problem = None

    def achieve_all(self):
        """Attempt to achieve all goals for the current problem.

        :rtype:  str
        :return: "SUCCESS" if the problem is solved, else "FAILURE".

        """
        for goal in self.goals:
            if not self.achieve(goal):
                return "FAILURE"

            # goal was achieved, store local state and ops, reset local ops
            self.update_solution_history(goal)

            # make sure any previously achieved goals were not clobbered
            if self.clobbers_previous_goals(goal):
                return "FAILURE"  # problem solution failed (sibling clobbered)

        # if we got this far, we have a working solution, so we can now apply
        # all the necessary operators to the initial state
        self.apply_solution()
        return "SUCCESS"

    def update_solution_history(self, goal):
        """Update the solution history for the given goal by storing its
        solution as the current value of the instance variable 'local_ops' and
        its state as the current value of 'local_state'.

        :type  goal: :class:Condition
        :param goal: The goal to update solution history for.

        """
        goal_history = self.solution_history[goal]
        goal_history['ops'] = self.local_ops
        goal_history['state'] = self.local_state
        self.local_ops = []  # reset local ops list

    def apply_solution(self):
        """Apply all operators in the solution history to solve the problem."""
        for goal in self.goals:
            map(self.apply_op, self.solution_history[goal]['ops'])

    def clobbers_previous_goals(self, goal):
        """Check to see if this goal clobbers previously achieved goals.

        :type  goal: :class:Condition
        :param goal: The goal to check.

        """
        current_goal_index = self.goals.index(goal)
        for previous_goal in self.goals[:current_goal_index]:
            # check for membership in this goal's solution state
            if previous_goal not in self.solution_history[goal]['state']:
                return True  # problem solution failed (sibling clobbered)

        return False

    def achieve(self, goal):
        """Attempt to achieve a particular goal.

        :type  goal: :class:Condition
        :param goal: The goal that we are attempting to achieve.
        :rtype:  bool
        :return: True if the goal was achieved, else False.

        """
        # case 1: base case (goal condition is in current state)
        if goal in self.local_state:
            return True

        # we need to return the sequence of operators in the opposite order from
        # that in which they are considered: because we start with the final
        # operation and end with the operation that satisfies the last
        # precondition
        #   --> this should be done in test_op

        # case 2: there exists some set of operations to put the goal condition
        # in the current state
        for op in self.ops:
            if self.is_appropriate(op, goal):
                self.test_op(op)
                return True

        return False

    def test_op(self, op):
        """Apply a particular operation by adding all conditions in its
        add-list and removing all in its delete-list. Only modify the
        local state -- that's what makes it a test. Will also need to
        ensure all preconditions can be achieved.

        :type  op: :class:Operation
        :param op: The operation to apply.

        """
        if (all(map(self.achieve, op.preconditions))):
            op.simulate(self.local_state)  # alter state but don't execute
            self.local_ops.append(op)  # track necessary ops for solution

    def apply_op(self, op):
        """Execute the operation, altering the current state.

        :type  op: :class:Operation
        :param op: The operation to apply.

        """
        op.execute(self.state)
