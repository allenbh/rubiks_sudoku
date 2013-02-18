
import cube
import fmt
import fileinput

# Transform problem using steps read from fileinput.
# Print the cube configuration after each step.

# This is useful if you solve a rubiks equivalent problem
# with a rubiks solver, and you want to manipulate the
# sudoku cube without getting lost in the middle.

problem = (
    6, 2, 1, 8, 1, 3, 5, 9, 3,
    8, 6, 6, 4, 3, 9, 5, 7, 3, 7, 8, 4,
    9, 7, 9, 2, 6, 3, 4, 4, 2, 6, 1, 8,
    7, 7, 2, 2, 8, 7, 9, 2, 9, 6, 5, 5,
    4, 5, 1, 4, 5, 1, 8, 3, 1)

transform_dict = dict(cube.turns)

print(fmt.fmt_cube(problem))
for line in fileinput.input():
  line = line.strip()
  trans = transform_dict[line]
  problem = cube.turn(problem, trans)
  print(line)
  print(fmt.fmt_cube(problem))

