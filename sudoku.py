
import cube
import fmt
import itertools
import random

# Indices:
#           0  1  2
#           3  4  5
#           6  7  8
#  9 10 11 12 13 14 15 16 17 18 19 20
# 21 22 23 24 25 26 27 28 29 30 31 32
# 33 34 35 36 37 38 39 40 41 42 43 44
#          45 46 47
#          48 49 50
#          51 52 53

def side_satisfied(side):
  '''Values occur at most once in the correct position'''

  seen = set()
  orient = None

  for (i, val) in enumerate(side):
    if val is not None:

      #(face_val, face_pos) = val
      face_val = val[0]
      face_pos = val[1]

      if face_pos is not None:
        if orient is None:
          for o in orients:
            if o[i] == face_pos:
              orient = o
              break
        elif orient[i] != face_pos:
          return False

      if face_val in seen:
        return False

      seen.add(face_val)

  return True


def cube_satisfied(state):
  '''Each side is satisfied'''
  for face in cube.faces:
    if not side_satisfied(cube.turn(state, face)):
      return False
  return True

# Cubelets:
#           a  b  c
#           d  -  e
#           f  g  h
#  a  d  f  f  g  h  h  e  c  c  b  a
#  i  -  j  j  -  k  k  -  l  l  -  i
#  m  n  o  o  p  q  q  r  s  s  t  m
#           o  p  q
#           n  -  r
#           m  t  s

centers = (4, 22, 25, 28, 31, 49)

corner_cubelets = (
    (0, 9, 20),
    (2, 17, 18),
    (6, 11, 12),
    (8, 14, 15),
    (33, 44, 51),
    (35, 36, 45),
    (38, 39, 47),
    (41, 42, 53))

edge_cubelets = (
    (1, 19),
    (3, 10),
    (5, 16),
    (7, 13),
    (21, 32),
    (23, 24),
    (26, 27),
    (29, 30),
    (34, 48),
    (37, 46),
    (40, 50),
    (43, 52))

# Center Orientation:
#  -  0  -
#  3  -  1
#  -  2  -

# Face Positions: (by orientation)
#
#  0  1  2   6  3  0   8  7  6   2  3  6
#  3  N  5   7  N  1   5  N  3   1  N  7
#  6  7  8   8  5  2   2  1  0   0  5  8

orient_0 = (0, 1, 2, 3, None, 5, 6, 7, 8)
orient_1 = cube.turn(orient_0, cube.face_cw)
orient_2 = cube.turn(orient_1, cube.face_cw)
orient_3 = cube.turn(orient_2, cube.face_cw)

orients = (orient_0, orient_1, orient_2, orient_3)

# Problem Definition: (each face)
#   corner and edge values: (face_val, face_pos)
#   center values: (face_val, None)

def satisfy_goals(goal,
    corner_cl, corner_vals,
    edge_cl, edge_vals):

  if not cube_satisfied(goal):
    return

  if not corner_cl and not edge_cl:
    yield tuple(goal)

  elif edge_cl:
    ec = edge_cl.pop(0)
    for ev_i in range(len(edge_vals)):
      ev = edge_vals.pop(ev_i)
      for evp in itertools.permutations(ev):
        for (i,v) in zip(ec,evp):
          goal[i] = v
        for x in satisfy_goals(goal,
            corner_cl, corner_vals, edge_cl, edge_vals):
          yield x
      edge_vals.insert(ev_i, ev)
    for i in ec:
      goal[i] = None
    edge_cl.insert(0, ec)

  else:
    cc = corner_cl.pop(0)
    for cv_i in range(len(corner_vals)):
      cv = corner_vals.pop(cv_i)
      for cvp in itertools.permutations(cv):
        for (i,v) in zip(cc,cvp):
          goal[i] = v
        for x in satisfy_goals(goal,
            corner_cl, corner_vals, edge_cl, edge_vals):
          yield x
      corner_vals.insert(cv_i, cv)
    for i in cc:
      goal[i] = None
    corner_cl.insert(0, cc)

def compute_goals(state):

  center_vals = cube.turn(state, centers)

  goal = [None]*54
  for (i,v) in zip(centers, center_vals):
    goal[i] = v

  corner_cl = list(corner_cubelets)

  corner_vals = (
      cube.turn(state, cc)
      for cc in corner_cl)

  corner_vals = list(corner_vals)
  random.shuffle(corner_vals)

  edge_cl = list(edge_cubelets)

  edge_vals = (
      cube.turn(state, ec)
      for ec in edge_cl)

  edge_vals = list(edge_vals)
  random.shuffle(edge_vals)

  return satisfy_goals(goal,
      corner_cl, corner_vals,
      edge_cl, edge_vals)

def sym_of(index, default=-1):
  def fun(v):
    try:
      val = v[index]
      if val is not None:
        return val
      return default
    except:
      return default
  return fun

def main():

  problem = (
      (6, 8), (2, 7), (1, 2), (8, 5), (1, None), (3, 5), (5, 6), (9, 5), (3, 0),
      (8, 6), (6, 3), (6, 6), (4, 8), (3, 7), (9, 6), (5, 8), (7, 3), (3, 0), (7, 6), (8, 1), (4, 8),
      (9, 1), (7, None), (9, 7), (2, 3), (6, None), (3, 5), (4, 1), (4, None), (2, 7), (6, 7), (1, None), (8, 7),
      (7, 2), (7, 1), (2, 2), (2, 2), (8, 3), (7, 2), (9, 8), (2, 3), (9, 0), (6, 2), (5, 1), (5, 6),
      (4, 0), (5, 5), (1, 0), (4, 3), (5, None), (1, 5), (8, 8), (3, 1), (1, 0))

  problem = tuple(map(lambda v: v[1]+(v[0],), enumerate(problem)))

  goals = list(compute_goals(problem))
  seen = set()

  print('Goals:')
  for g in goals:
    g = tuple(map(sym_of(0), g))
    if g in seen:
      continue
    seen.add(g)
    print(fmt.fmt_cube(g))
    print()

  print('Orients:')
  for g in goals:
    g = tuple(map(sym_of(1,4), g))
    if g in seen:
      continue
    seen.add(g)
    print(fmt.fmt_cube(g))
    print()

  def invert(g):
    table = {v:i for (i,v) in enumerate(g)}
    state = tuple((table[i] for i in range(54)))
    return state

  print('Indices:')
  for g in goals:
    g = invert(map(sym_of(2), g))
    if g in seen:
      continue
    seen.add(g)
    print(fmt.fmt_cube(g))
    print()

  face_lift = (
      1, 1, 1, 1, 1, 1, 1, 1, 1,
      2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5,
      2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5,
      2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5,
      6, 6, 6, 6, 6, 6, 6, 6, 6)

  print('Rubix Equivalent:')
  for g in goals:
    g = invert(map(sym_of(2), g))
    g = tuple(map(face_lift.__getitem__, g))
    if g in seen:
      continue
    seen.add(g)
    print(fmt.fmt_cube(g))
    print()

if __name__ == '__main__':
  main()

