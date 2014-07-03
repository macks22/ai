## Overview

The General Problem Solver (GPS) was developed in 1957 by Alan Newell and
Herbert Simon to be a single computer program capable of solving any problem
when given a suitable description of the problem.

### Means-ends Analysis

The method of problem-solving used by the GPS is means-ends analysis.
Aristotle wrote what is perhaps the most elegant formulation of the theory
of means-ends analysis in the chapter entitled "The nature of deliberation
and its objects" of the Nicomachean Ethics (Book III.3,1112b):

> We deliberate not about ends, but about means. For a doctor does not
deliberate whether he shall heal, nor an orator whether he shall persuade,
nor a statesman whether he shall produce law and order, nor does any one
else deliberate about his end. They assume the end and consider how and by
what means it is attained; and if it seems to be produced by several means
they consider by which it is most easily and best produced, while if it is
achieved by one only they consider how it will be achieved by this and by
what means this will be achieved, till they come to the first cause, which
in the order of discovery is last... and what is last in the order of
analysis seems to befirst in the order of becoming.  And if we come on an
impossibility, we give up the search, e.g., if we need money and this cannot
be got; but if a thing appears possible we try to do it.

## Description

1.  The process of solving the problem is stated in terms of what we want to
    happen (the end).
2.  We must discover some path to our solution (the means).
    1. some way to eliminate "the difference between what I have
       and what I want."
3.  Some actions (means) may require the solving of preconditions as
    subproblems. Before we can do A we must do B (or perhaps B, C, and D).
    1. A problem is either solved directly (base case)
    2. or by first solving the subproblem (recursion)
4.  An action is _appropriate_ to take if it leads us towards our ends.
    1. we will need some description of allowable actions
    2. each action must be composed of
        1. preconditions
        2. effects

## Specification

*   We can represent the state of the world as sets of conditions
    + what I have (set called 'state')
    + what I want (set called 'goal')
*   We need a list of allowable operators
    + constant over the course of a problem
    + dynamic across problems
*   Operator (op) can be represented as a class
    + an action
    + a set of preconditions
    + a set of effects (add/delete from 'state' to get to 'goal')
        - can be split into add_list and delete_list (STRIPS approach)
*   Complete problem described by: gps((unknown, poor), (rich,famous) ops)
    1. starting state
    2. goal state
    3. set of known operators
*   Approach to solving a problem: go through conditions in goal state one at a
    time and try to achieve each one. If all can be achieved, problem solved.
*   Single goal condition can be achieved in two ways:
    1. if it is already the current state (trivial case)
    2. find some appropriate op and try to apply it
*   Op is _appropriate_ if one of the effects is to add the goal in question to
    the current state (appropriate if goal condition in add_list)
*   An op can be applied if we can achieve all preconditions
    + this may be trivial when the action is something as simple as printing

## Implementation

The object-oriented implementation of the GPS is
[here](https://github.com/macks22/ai/blob/master/gps/gps.py).

You can find the class diagram for it
[here](https://github.com/macks22/ai/blob/master/gps/docs/class-diagram.png).

See the [Drive To School Problem](https://github.com/macks22/ai/blob/master/gps/problems/drive_to_school.py)
for an example of how to formulate a problem. To solve this problem, execute
these expressions in an interpreter:

    import gps
    solver = gps.GPS()
    from problems import drive_to_school
    solver.solve(drive_to_school.PROBLEM)

Alternatively, with the CLI:

    python solve.py problems/drive_to_school.py

## Limitations of the Initial Approach

###  Running Around the Block Problem

What should GPS do if there is no net change resulting from performing an
action? Perhaps add-list should contain something like "got exercise" or
"feel tired."

### Clobbered Sibling Goal Problem

_aka Prerequisite Clobbers Sibling Goal_

If one goal is achieved and then the next is achieved, the achieving of the
second goal might wipe out the results of the first. This is a situation the
naieve GPS will ignore, but it is conceptually wrong. Both goals should remain
achieved if the problem is said to be "solved."

To enhance the idea of solving a problem we must add the condition that every
goal can be achieved and the set of conditions which are goals must be a subset
of the conditions present in the state at the end of the process.

### Leaping Before You Look Problem

When there is more than one goal condition, the program might execute the
operations necessary to achieve one goal, only to find that a subsequent goal
cannot be achieved. (jump-off-cliff land-safely) ==> program first jumps off
cliff only to find afterwards that there is no way to land safely. This problem
comes from the interleaving of planning and execution - state is irrevocably
changed before all goals are evaluated.

To solve the problem, we must maintain a local state for each particular
subproblem being evaluated.

### Recursive Subgoal Problem

Can have situations which end up leading to infinite oscillation between a means
and an end. For instance:

    end: shop-knows-problem
    means: in-communication-with-shop
    precondition: know-phone-number

    end: know-phone-number
    means: in-communication-with-shop

One way to solve the problem is to keep a list of operations and detect loops in
the inference process.

### Lack of Intermediate Information Problem

When the GPS fails to find a problem, it simply returns NIL, which is fairly
useless for debugging cases where a solution should have been found. We should
modify the program to log reasoning output as debug info.

## Modifications to Address Limitations (GPSv2)

1.  store local state variable for each individual goal
2.  all functions take current state and return new/unchanged state
3.  can use some marker "start" to disambiguate between valid states that have
    no conditions and failure.
4.  introduce a goal stack to solve recursive subgoal problem
    * keep track of goals it is working on; immediately fails if a goal appears
      as a subgoal of itself.
