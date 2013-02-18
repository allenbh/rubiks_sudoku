
import cube
import fmt
import random
import sudoku
import sys
import time


def solve(goals, state):

  path = []
  step = goals[state]

  while step is not None:

    path.append(step)
    step = goals[step[1]]

  path.reverse()

  return path


def search(state, depth, goals, paths, closed):

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

  goals = {goal: None for goal in goal_list}
  paths = {state: None}

  closed_1 = {}
  closed_2 = {}

  for depth_i in range(depth//2 + depth%2 + 1):
    print('search forward at depth:', depth_i, file=sys.stderr)
    start = time.clock()
    result = search(state, depth_i, goals, paths, closed_1)
    #print('expanded nodes:', len(closed_1), file=sys.stderr)
    #print('cpu seconds:', time.clock() - start, file=sys.stderr)
    if result is not None:
      result.reverse()
      return result

    for (goal_i, goal) in enumerate(goal_list):
      print('search backward from goal:', goal_i, file=sys.stderr)
      start = time.clock()
      result = search(goal, depth_i, paths, goals, closed_2)
      #print('expanded nodes:', len(closed_2), file=sys.stderr)
      #print('cpu seconds:', time.clock() - start, file=sys.stderr)
      if result is not None:
        return result


def randomize(state, depth):
  path = []
  while depth > 0:
    depth -= 1
    step = random.choice(list(cube.expand(state)))
    state = step[1]
  return (state, path)


problem = (
    6, 2, 1, 8, 1, 3, 5, 9, 3,
    8, 6, 6, 4, 3, 9, 5, 7, 3, 7, 8, 4,
    9, 7, 9, 2, 6, 3, 4, 4, 2, 6, 1, 8,
    7, 7, 2, 2, 8, 7, 9, 2, 9, 6, 5, 5,
    4, 5, 1, 4, 5, 1, 8, 3, 1)

sudoku_problem = (
    (6, 8), (2, 7), (1, 2), (8, 5), (1, None), (3, 5), (5, 6), (9, 5), (3, 0),
    (8, 6), (6, 3), (6, 6), (4, 8), (3, 7), (9, 6), (5, 8), (7, 3), (3, 0), (7, 6), (8, 1), (4, 8),
    (9, 1), (7, None), (9, 7), (2, 3), (6, None), (3, 5), (4, 1), (4, None), (2, 7), (6, 7), (1, None), (8, 7),
    (7, 2), (7, 1), (2, 2), (2, 2), (8, 3), (7, 2), (9, 8), (2, 3), (9, 0), (6, 2), (5, 1), (5, 6),
    (4, 0), (5, 5), (1, 0), (4, 3), (5, None), (1, 5), (8, 8), (3, 1), (1, 0))

depth = 10

print('Start state:')
print(fmt.fmt_cube(problem))

config_random = True
goal_list = None

if config_random:
  goal_list = [randomize(problem, depth)[0]]
else:
  sudoku_goals = sudoku.compute_goals(sudoku_problem)
  goal_list = set()
  for s_goal in sudoku_goals:
    goal = tuple(map(lambda v: v[0], s_goal))
    goal_list.add(goal)
  goal_list = list(goal_list)

print('Goal states:')
for goal in goal_list:
  print(fmt.fmt_cube(goal))

solution = None
start_i = 0

solution = deep_search_2d(problem, goal_list, depth)

if solution is None:
  print('No solution found.')
else:
  print('Solution:')
  print(fmt.fmt_cube(problem))
  for (sym,child) in solution:
    print(sym)
    print(fmt.fmt_cube(child))
  print('Solved in', len(solution), 'steps!')


