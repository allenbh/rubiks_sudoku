
import cube
import fmt
import random
import sudoku
import sys
import time
from itertools import chain
from operator import itemgetter


def solve(goals, state):
  '''Compute the path from a goal to the starting state.
  
  Parameters:
    goals   - closing book for finding a goal
    state   - start state (must exist in the goals table)
    
  Returns:
    [(sym, state), ...] - reversed list of transitions from start state to goal'''

  assert state in goals, 'Starting state must exist in the closing book'

  path = []
  step = goals[state]

  while step is not None:

    path.append(step)
    step = goals[step[1]]

  path.reverse()

  return path


def invert_path(path, goal):
  '''Reverse the path shifting by one for the goal, and invert transitions.

  Parameters:
    path    - reversed list of transitions from goal to start state
    goal    - goal state, absent in reverse solution

  Returns:
    [(sym, state), ...] - reversed list of transitions from start state to goal'''

  syms = map(itemgetter(0), reversed(path))
  syms = map(cube.invert_sym, syms)

  states = map(itemgetter(1), reversed(path[1:]))
  states = chain((goal,), states)

  path = list(zip(syms,states))

  return path


def search(state, depth, goals, paths, closed):
  '''Perform depth first search starting from state to any goal.
  
  Parameters:
    state   - starting state for search
    depth   - limit for depth first search
    goals   - closing book for finding a goal
    paths   - closing book for search in opposite direction
    closed  - closed list for pruning symmetric states
    
  Returns:
    None                - no solution
    [(sym, state), ...] - reversed list of transitions from start state to goal'''

  closed[state] = depth

  if state in goals:
    return solve(goals, state)

  if depth <= 0:
    return None
  depth -= 1

  for (sym, child) in cube.expand(state):

    if child in closed and depth <= closed[child]:
      continue

    if child not in paths:
      paths[child] = (cube.invert_sym(sym), state)

    result = search(child, depth, goals, paths, closed)

    if result is not None:
      result.append((sym,child))
      return result


def deep_search_2d(state, goal_list, depth):
  '''Perform iterative deepening bidirectional search from state to any goal.

  Parameters:
    state       - starting state for search
    goal_list   - list of acceptable goal states
    depth       - maximum allowed depth for search

  Returns:
    None                - no solution
    [(sym, state), ...] - reversed list of transitions from start state to goal'''

  if not goal_list:
    print('Empty goal list.', file=sys.stderr)
    return None

  goals = {goal: None for goal in goal_list}
  paths = {state: None}

  closed_1 = {}
  closed_2 = {}

  for depth_i in range(1, depth//2 + depth%2 + 1):
    print('Search forward at depth:', depth_i, file=sys.stderr)
    #start = time.clock()
    result = search(state, depth_i, goals, paths, closed_1)
    #print('expanded nodes:', len(closed_1), file=sys.stderr)
    #print('cpu seconds:', time.clock() - start, file=sys.stderr)
    if result is not None:
      print('Found a solution.', file=sys.stderr)
      return result

    for (goal_i, goal) in enumerate(goal_list):
      print('Search backward from goal:', goal_i, file=sys.stderr)
      #start = time.clock()
      result = search(goal, depth_i, paths, goals, closed_2)
      #print('expanded nodes:', len(closed_2), file=sys.stderr)
      #print('cpu seconds:', time.clock() - start, file=sys.stderr)
      if result is not None:
        print('Found a solution.', file=sys.stderr)
        return invert_path(result, goal)


def randomize(state, depth):
  '''Random walk staring from state for depth number of steps.

  Parameters:
    state       - starting state for walk
    depth       - number of steps in the path

  Returns:
    (state, path) - final state and path walked'''

  path = []

  while depth > 0:
    depth -= 1
    step = random.choice(list(cube.expand(state)))
    state = step[1]

  return (state, path)


if __name__ == '__main__':

  # maximum search depth
  #   this program rounds the search depth up to next even number
  #   this program doesn't use heuristics to limit the search
  #   depths greater than 12 start to get impractical
  depth = 10

  # config_random:
  #   zero - solve sudoku cube
  #   positive - solve sudoku cube to a random goal
  #     (odd length solutions are found in forward search,
  #       even length solutions are found in backwards search)
  config_random = 10

  problem = None
  goal_list = None

  if config_random:
    goal = tuple(range(54))
    problem = randomize(goal, config_random)[0]
    goal_list = [goal]

  else:
    # Read sudoku.py for how to build a sudoku problem

    #sudoku_problem = (
    #    (6, 8), (2, 7), (1, 2), (8, 5), (1, None), (3, 5), (5, 6), (9, 5), (3, 0),
    #    (8, 6), (6, 3), (6, 6), (4, 8), (3, 7), (9, 6), (5, 8), (7, 3), (3, 0), (7, 6), (8, 1), (4, 8),
    #    (9, 1), (7, None), (9, 7), (2, 3), (6, None), (3, 5), (4, 1), (4, None), (2, 7), (6, 7), (1, None), (8, 7),
    #    (7, 2), (7, 1), (2, 2), (2, 2), (8, 3), (7, 2), (9, 8), (2, 3), (9, 0), (6, 2), (5, 1), (5, 6),
    #    (4, 0), (5, 5), (1, 0), (4, 3), (5, None), (1, 5), (8, 8), (3, 1), (1, 0))

    sudoku_problem = (
        (8, 6), (4, 1), (3, 0), (8, 7), (7, None), (5, 1), (9, 8), (1, 5), (2, 2),
        (4, 8), (9, 1), (7, 2), (1, 0), (2, 3), (2, 2), (4, 0), (3, 1), (7, 6), (1, 2), (3, 5), (6, 8),
        (9, 7), (1, None), (5, 5), (8, 3), (1, None), (3, 5), (7, 3), (5, None), (3, 7), (9, 5), (6, None), (2, 3),
        (7, 2), (2, 7), (4, 8), (6, 6), (8, 5), (5, 8), (9, 6), (2, 7), (1, 0), (9, 0), (4, 3), (5, 6),
        (5, 6), (6, 3), (3, 0), (6, 7), (4, None), (8, 1), (8, 8), (7, 1), (6, 2))

    #problem = (
    #    6, 2, 1, 8, 1, 3, 5, 9, 3,
    #    8, 6, 6, 4, 3, 9, 5, 7, 3, 7, 8, 4,
    #    9, 7, 9, 2, 6, 3, 4, 4, 2, 6, 1, 8,
    #    7, 7, 2, 2, 8, 7, 9, 2, 9, 6, 5, 5,
    #    4, 5, 1, 4, 5, 1, 8, 3, 1)

    problem = tuple(map(lambda v: v[0], sudoku_problem))

    sudoku_goals = sudoku.compute_goals(sudoku_problem)
    goal_list = set()
    for s_goal in sudoku_goals:
      goal = tuple(map(lambda v: v[0], s_goal))
      goal_list.add(goal)
    goal_list = list(goal_list)

  print('Start state:')
  print(fmt.fmt_cube(problem))

  print('Goal states:')
  for goal in goal_list:
    print(fmt.fmt_cube(goal))

  solution = deep_search_2d(problem, goal_list, depth)

  if solution is None:
    print('No solution found.')
  else:
    print('Solution:')
    print(fmt.fmt_cube(problem))
    for (sym,child) in reversed(solution):
      print(sym)
      print(fmt.fmt_cube(child))
    print('Solved in', len(solution), 'steps!')


