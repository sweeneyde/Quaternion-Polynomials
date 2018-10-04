import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def plot(quat_list):
    coordinate = lambda index: [q[index] for q in quat_list]
    c = coordinate(0)
    x = coordinate(1)
    y = coordinate(2)
    z = coordinate(3)

    print("plotting...")

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect("equal")
    pnt3d = ax.scatter(x, y, z, c=c, cmap=plt.viridis())

    # def draw_sphere(r, color):
    #     u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    #     x = np.cos(u) * np.sin(v)
    #     y = np.sin(u) * np.sin(v)
    #     z = np.cos(v)
    #     ax.plot_wireframe(r * x, r * y, r * z)
    #     # TODO: fix color
    #
    #
    # for a, b, _, _ in solution_classes:
    #     draw_sphere(r=b, color=a)

    cbar = plt.colorbar(pnt3d)
    cbar.set_label("Real Part")

    #Make sure the axes have equal scale, centered at 0.
    M = max(abs(q) for q in x+y+z)
    ax.plot([-M], [-M], [-M], 'w')
    ax.plot([M], [M], [M], 'w')

    ax.set_xlabel("i")
    ax.set_ylabel("j")
    ax.set_zlabel("k")

    plt.show()
