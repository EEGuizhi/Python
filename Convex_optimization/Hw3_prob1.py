# 4109061012 B.S.Chen
"""
# Problem description:
- Table:
    Food ||  Cost  | Vitamin | Calories
    -----------------------------------
      x1 ||  0.18  |   107   |    72
      x2 ||  0.23  |   500   |   121
      x3 ||  0.05  |    0    |    65
- Restrictions:
    1. 2000 <= 72*x1 + 121*x2 + 65*x3 <= 2250
    2. 5000 <= 107*x1 + 500*x2 + 0*x3 <= 50000
    3. x1, x2, x3 <= 10
    4. x1, x2, x3 >= 0
- Goal:
    Minimize cost (= 0.18*x1 + 0.23*x2 + 0.05*x3)
"""
import numpy as np
import cvxpy as cp

# Settings
vec_C = np.array([0.18, 0.23, 0.05]).T
mat_A = np.array([
    [  72,  121,  63],
    [ -72, -121, -63],
    [ 107,  500,   0],
    [-107, -500,   0],
    [   1,    0,   0],
    [   0,    1,   0],
    [   0,    0,   1],
    [  -1,    0,   0],
    [   0,   -1,   0],
    [   0,    0,  -1]
])
vec_B = np.array([2250, -2000, 50000, -5000, 10, 10, 10, 0, 0, 0]).T

# Solve
x = cp.Variable(3)
prob = cp.Problem(cp.Minimize(vec_C.T @ x), [mat_A @ x <= vec_B])
prob.solve()

# Show result
print(f">> Ans: x1(C) = {round(x.value[0], 3)}, x2(M) = {round(x.value[1], 3)}, x3(W) = {round(x.value[2], 3)}")
print(f">> Optimal value p* = {round(vec_C.T @ x.value, 3)}")
