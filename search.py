
import cube
import fmt

def side_goal(side):
  seen = set()
  for val in side:
    if val in seen:
      return False
    seen.add(val)
  return True

def goal(state):
  for face in cube.faces:
    if not side_goal(cube.turn(state, face)):
      return False
  return True

closed_limit = 1000000

def search(state, depth, closed = {}):
  if goal(state):
    return []
  if depth <= 0:
    return None
  if state in closed:
    return None
  if len(closed) < closed_limit:
    closed[state] = depth
  depth -= 1
  for (sym,child) in cube.expand(state):
    if child in closed:
      continue
    result = search(child, depth, closed)
    if result is not None:
      result.append((sym,child))
      return result

def deep_search(state, depth_limit):
  for depth in range(depth_limit):
    result = search(state, depth)
    if result is not None:
      return result

problem = tuple(range(54))
print(fmt.fmt_cube(problem))

limit = 18 
solution = deep_search(problem, limit)

if solution is None:
  print('No solution found')
else:
  for (sym,child) in reversed(solution):
    print(sym)
    print(fmt.fmt_cube(child))
  print('Solved!')


