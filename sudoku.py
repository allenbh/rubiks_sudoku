
import cube
import fmt
import itertools
import random
from copy import deepcopy
from operator import itemgetter

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

val_key = 0
pos_key = 1
orient_key = None
index_key = None

def side_satisfied(side):
  '''Values occur at most once in the correct position'''

  seen = set()
  orient = None
  orient_index = None

  for (i, val) in enumerate(side):
    if val is not None:

      #(face_val, face_pos) = val
      face_val = val[val_key]
      face_pos = val[pos_key]

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

# Face Orientations:
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

def orient_goal(goal):
  '''Record the orientation of each face'''
  if orient_key is None:
    return goal

  goal = deepcopy(goal)

  for face in cube.faces:
    side = cube.turn(goal, face)
    orient_index = None
    for (i, o) in enumerate(orients):
      if o[0] == side[0][pos_key]:
        orient_index = i
        break
    for v in side:
      v[orient_key] = orient_index

  return goal


def satisfy_goals(goal,
    corner_cl, corner_vals,
    edge_cl, edge_vals):
  '''Find configurations that satisfy the sudoku constraint on each side'''

  if not cube_satisfied(goal):
    return

  if not corner_cl and not edge_cl:
    yield tuple(orient_goal(goal))

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
  '''Find configurations that satisfy the sudoku constraint on each side'''

  center_vals = cube.turn(state, centers)

  partial_goal = [None]*54
  for (i,v) in zip(centers, center_vals):
    partial_goal[i] = v

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

  return satisfy_goals(partial_goal,
      corner_cl, corner_vals,
      edge_cl, edge_vals)


if __name__ == '__main__':

  # Problem Definition:
  #   corner and edge values: (face_val, oriented face_pos)
  #   center values: (face_val, None)
  #
  #   face_val - the number printed on the sticker
  #   face_pos - where on the face the number appears when it is oriented
  #               (When number is in the natural orientation, top-side-up,
  #                 where does it appear on the cube face?
  #                 - upper left, right edge, etc.
  #                 - the value is the corresponding number in orientation zero

  problem = (
      (6, 8), (3, 7), (5, 6), (8, 3), (7, None), (3, 5), (6, 6), (9, 7), (5, 8),
      (8, 6), (5, 5), (4, 8), (5, 6), (2, 3), (3, 0), (9, 6), (7, 3), (8, 8), (7, 2), (9, 5), (4, 8),
      (9, 1), (1, None), (2, 7), (6, 7), (1, None), (5, 1), (3, 1), (5, None), (2, 7), (8, 1), (6, None), (8, 7),
      (3, 0), (6, 3), (7, 2), (9, 8), (3, 5), (2, 2), (4, 0), (1, 5), (6, 2), (1, 0), (4, 3), (7, 6),
      (1, 0), (4, 1), (2, 2), (8, 5), (4, None), (2, 3), (1, 2), (7, 1), (9, 0))


  # Extend the problem definition for extra analysis

  val_key = 'val'
  pos_key = 'pos'
  orient_key = 'orient'
  index_key = 'index'

  problem = tuple(map(
    lambda v: {
      val_key : v[1][0],
      pos_key : v[1][1],
      index_key : v[0]},
    enumerate(problem)))


  goals = list(compute_goals(problem))

  print('Goals:')
  seen = set()
  for g in goals:
    g = tuple(map(itemgetter(val_key), g))
    if g in seen:
      continue
    seen.add(g)
    print(fmt.fmt_cube(g))
    print()

  def default(n):
    def fun(x):
      if x is None:
        return n
      return x
    return fun

  print('Face Positions:')
  seen = set()
  for g in goals:
    g = map(itemgetter(pos_key), g)
    g = tuple(map(default(4), g))
    if g in seen:
      continue
    seen.add(g)
    print(fmt.fmt_cube(g))
    print()

  print('Face Orientations:')
  seen = set()
  for g in goals:
    g = tuple(map(itemgetter(orient_key), g))
    if g in seen:
      continue
    seen.add(g)
    print(fmt.fmt_cube(g))
    print()

  def invert(g):
    table = {v:i for (i,v) in enumerate(g)}
    state = tuple((table[i] for i in range(54)))
    return state

  print('Inverted indices:')
  seen = set()
  for g in goals:
    g = invert(map(itemgetter(index_key), g))
    if g in seen:
      continue
    seen.add(g)
    print(fmt.fmt_cube(g))
    print()

  face_tbl = (
      1, 1, 1, 1, 1, 1, 1, 1, 1,
      2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5,
      2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5,
      2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5,
      6, 6, 6, 6, 6, 6, 6, 6, 6)

  print('Rubiks Equivalent:')
  seen = set()
  for g in goals:
    g = invert(map(itemgetter(index_key), g))
    g = tuple(map(face_tbl.__getitem__, g))
    if g in seen:
      continue
    seen.add(g)
    print(fmt.fmt_cube(g))
    print()

