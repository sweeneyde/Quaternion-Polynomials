from random import uniform, gauss
from itertools import product
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from pyquaternion import Quaternion as Q
from quat_poly import quat_poly



def all_signs_qp():
    for c in product((-1, 0, 1), repeat=degree * 4):
        yield [Q(c[i], c[i + 1], c[i + 2], c[i + 3]) for i in range(0, degree, 4)]


def uniform_random_qp(smallest, biggest, number):
    r = lambda: uniform(smallest, biggest)
    for _ in range(number):
        yield [Q(r(), r(), r(), r()) for _ in range(degree)]


def gaussian_random_qp(number):
    r = lambda: gauss(0, 10)
    for _ in range(number):
        yield [Q(r(), r(), r(), r()) for _ in range(degree)]


degree = 3
polynomial_generator = all_signs_qp()

individual_solutions = [] #set()
solution_classes = set()

for i, coefficients in enumerate(polynomial_generator):
    if i % 10000 == 0:
        print(i / 531441)  # show progress on long loops

    # Construct a monic quaternion polynomial:
    p = quat_poly(*coefficients, 1)

    inds, cls = p.roots()
    individual_solutions += [(a, b, c, d) for (a, b, c, d) in inds]
    solution_classes |= set((a, b, c, d) for (a, b, c, d) in cls)

coordinate = lambda index: [q[index] for q in individual_solutions]
c = coordinate(0)
x = coordinate(1)
y = coordinate(2)
z = coordinate(3)

print("plotting...")

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")
pnt3d = ax.scatter(x, y, z, c=c, cmap=plt.viridis())


def draw_sphere(r, color):
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_wireframe(r * x, r * y, r * z)
    # TODO: fix color


for a, b, _, _ in solution_classes:
    draw_sphere(r=b, color=a)

cbar = plt.colorbar(pnt3d)
cbar.set_label("Real Part")

ax.set_xlabel("i")
ax.set_ylabel("j")
ax.set_zlabel("k")

plt.show()
