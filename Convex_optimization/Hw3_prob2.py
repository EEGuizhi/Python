# 4109061012 B.S.Chen
"""
# Problem description:
- Goal:
    Maximize r (= 0*x + 0*y + 1*r)
- Subject to:
    1. 5*x + 8*y + ((5^2 + 8^2)^(1/2))*r <= 50
    2. (-2)*x + 1*y + ((2^2 + 1^2)^(1/2))*r <= 1
    3. (-1)*x + 0*y + 1*r <= 0
    4. 0*x + (-1)*y + 1*r <= 0
"""
# import numpy
import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt

# Settings
a = (5**2 + 8**2)**(1/2)
b = (2**2 + 1**2)**(1/2)
vec_C = np.array([0, 0, 1]).T
mat_A = np.array([
    [ 5,  8,  a],
    [-2,  1,  b],
    [-1,  0,  1],
    [ 0, -1,  1]
])
vec_B = np.array([50, 1, 0, 0]).T

# Solve
var = cp.Variable(3)
prob = cp.Problem(cp.Maximize(vec_C.T @ var), [mat_A @ var <= vec_B])
prob.solve()

# Show result
x, y, r = var.value[0], var.value[1], var.value[2]
print(f">> Ans: x1(x) = {round(x, 3)}, x2(y) = {round(y, 3)}, x3(r) = {round(r, 3)}")
print(f">> Inscribed ball's radius r = {round(r, 3)}")

# Plot
plt.figure(figsize=(6, 6))
plt.plot(x, y, marker='x', label=f"center = ({round(x, 2)}, {round(y, 2)})")

theta = np.linspace(0, 2*np.pi, 300)
rx, ry = r * np.cos(theta), r * np.sin(theta)
plt.plot(rx + x, ry + y, label="inscribed ball")

linex = np.linspace(x - 10, x + 10, 300)
liney = (50 - 5 * linex) / 8
plt.plot(linex, liney, label="5x + 8y = 50")
liney = 2 * linex + 1
plt.plot(linex, liney, label="2x - y = -1")
linex, liney = np.linspace(0, 0, 300), np.linspace(y - 10, y + 10, 300)
plt.plot(linex, liney, label="x = 0")
linex, liney = np.linspace(x - 10, x + 10, 300), np.linspace(0, 0, 300)
plt.plot(linex, liney, label="y = 0")

plt.xlim(x - 10, x + 10), plt.ylim(y - 10, y + 10), plt.legend(), plt.show()
