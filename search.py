
import cube
import fmt
import random
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


def deep_search_2d(state, goal, depth):

  goals = {goal: None}
  paths = {state: None}

  closed_1 = {}
  closed_2 = {}

  for depth_i in range(depth//2 + depth%2 + 1):
    print('search 1 at depth:', depth_i, file=sys.stderr)
    start = time.clock()
    result = search(state, depth_i, goals, paths, closed_1)
    print('expanded nodes:', len(closed_1), file=sys.stderr)
    print('cpu seconds:', time.clock() - start, file=sys.stderr)
    if result is not None:
      result.reverse()
      return result

    print('search 2 at depth:', depth_i, file=sys.stderr)
    start = time.clock()
    result = search(goal, depth_i, paths, goals, closed_2)
    print('expanded nodes:', len(closed_2), file=sys.stderr)
    print('cpu seconds:', time.clock() - start, file=sys.stderr)
    if result is not None:
      return result


def randomize(state, depth):
  while depth > 0:
    depth -= 1
    state = random.choice(list(cube.expand(state)))[1]
  return state


problem = (
    6, 2, 1, 8, 1, 3, 5, 9, 3,
    8, 6, 6, 4, 3, 9, 5, 7, 3, 7, 8, 4,
    9, 7, 9, 2, 6, 3, 4, 4, 2, 9, 1, 8,
    7, 7, 2, 2, 8, 7, 9, 2, 9, 6, 5, 5,
    4, 5, 1, 4, 5, 1, 8, 3, 1)

depth = 5

print('Start state:')
print(fmt.fmt_cube(problem))

#goal = sudoku.solve(problem)
goal = randomize(problem, depth)

print('Goal state:')
print(fmt.fmt_cube(goal))

solution = deep_search_2d(problem, goal, depth)

if solution is None:
  print('No solution found.')
else:
  print('Solution:')
  print(fmt.fmt_cube(problem))
  for (sym,child) in solution:
    print(sym)
    print(fmt.fmt_cube(child))
  print('Solved in', len(solution), 'steps!')


