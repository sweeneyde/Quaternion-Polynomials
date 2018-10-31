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

    # plt.style.use('dark_background')
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect("equal")
    pnt3d = ax.scatter(x, y, z, c=c, cmap=plt.cm.get_cmap("viridis"), depthshade=False, marker=',', s=1)

    # def draw_sphere(r, color):
    #     u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    #     x = np.cos(u) * np.sin(v)
    #     y = np.sin(u) * np.sin(v)
    #     z = np.cos(v)
    #     ax.plot_wireframe(r * x, r * y, r * z)
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

if __name__ == "__main__":
    from polynomial_generators import ball_random_qp
    # Use the same generator, but instead but instead of plotting the roots,
    # just plot all of the coefficients (concatenate all of the lists)
    plot(sum(ball_random_qp(degree=2, number=500, radius=10), []))
