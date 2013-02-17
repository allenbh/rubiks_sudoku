
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

def turn(cube, trans):
  '''Rearrange the contents of the cube to the transformation indices'''
  return tuple(map(cube.__getitem__, trans))

def invert(trans):
  '''Compute the inverse transformation indices'''
  return turn(turn(trans, trans), trans)

# Faces:
#           U  U  U
#           U  U  U
#           U  U  U
#  L  L  L  F  F  F  R  R  R  B  B  B
#  L  L  L  F  F  F  R  R  R  B  B  B
#  L  L  L  F  F  F  R  R  R  B  B  B
#           D  D  D
#           D  D  D
#           D  D  D

face_U = (0, 1, 2, 3, 4, 5, 6, 7, 8)
face_L = (9, 10, 11, 21, 22, 23, 33, 34, 35)
face_F = (12, 13, 14, 24, 25, 26, 36, 37, 38)
face_R = (15, 16, 17, 27, 28, 29, 39, 40, 41)
face_B = (18, 19, 20, 30, 31, 32, 42, 43, 44)
face_D = (45, 46, 47, 48, 49, 50, 51, 52, 53)

edge_U = (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
edge_L = (20, 32, 44, 51, 48, 45, 36, 24, 12, 6, 3, 0)
edge_F = (8, 7, 6, 11, 23, 35, 45, 46, 47, 39, 27, 15)
edge_R = (2, 5, 8, 14, 26, 38, 47, 50, 53, 42, 30, 18)
edge_B = (0, 1, 2, 17, 29, 41, 53, 52, 51, 33, 21, 9)
edge_D = (44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33)

# Transformations:

edge_cw = (3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2)
face_cw = (6, 3, 0, 7, 4, 1, 8, 5, 2)

def compose(face, edge):
  '''Build a whole cube transformation from face and edge'''
  ident = range(54)
  trans = list(range(54))
  face_turn = turn(face, face_cw)
  edge_turn = turn(edge, edge_cw)
  for (i,t) in zip(face, face_turn):
    trans[i] = ident[t]
  for (i,t) in zip(edge, edge_turn):
    trans[i] = ident[t]
  return tuple(trans)

turn_U = compose(face_U, edge_U)
turn_L = compose(face_L, edge_L)
turn_F = compose(face_F, edge_F)
turn_R = compose(face_R, edge_R)
turn_B = compose(face_B, edge_B)
turn_D = compose(face_D, edge_D)

turn_cU = invert(turn_U)
turn_cL = invert(turn_L)
turn_cF = invert(turn_F)
turn_cR = invert(turn_R)
turn_cB = invert(turn_B)
turn_cD = invert(turn_D)

turns = (
    ("U", turn_U),
    ("U'", turn_cU),
    ("L", turn_L),
    ("L'", turn_cL),
    ("F", turn_F),
    ("F'", turn_cF),
    ("R", turn_R),
    ("R'", turn_cR),
    ("B", turn_B),
    ("B'", turn_cB),
    ("D", turn_D),
    ("D'", turn_cD))

def expand(cube):
  '''Return all turn symbols with respective turned cubes'''
  for (sym, trans) in turns:
    yield (sym, turn(cube, trans))

