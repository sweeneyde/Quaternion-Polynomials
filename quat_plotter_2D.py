import numpy as np
import matplotlib.pyplot as plt


def plot_2D(quat_list, x_axis_index=1, y_axis_index=2, color_axis_index=0, save_file=None, max_scale=None, title=None):
    coordinate = lambda index: [q[index] for q in quat_list]
    c = coordinate(color_axis_index)
    x = coordinate(x_axis_index)
    y = coordinate(y_axis_index)

    print("plotting...")

    plt.style.use('dark_background')
    fig = plt.figure()
    ax = fig.gca()
    ax.set_aspect("equal")


    #Make sure the axes have equal scale, centered at 0.
    if max_scale is None:
        M = max(abs(q) for q in x+y)
    else:
        M = max_scale

    pnt2d = ax.scatter(x, y, c=c, cmap=plt.bwr(), vmin=-M, vmax=M, marker=',', s=1)

    ax.plot([-M], [-M], 'w')
    ax.plot([M], [M], 'w')

    labels = ["Real Part", "i", "j", "k"]
    cbar = plt.colorbar(pnt2d)
    cbar.set_label(labels[color_axis_index])
    if title is not None:
        plt.title(title)
    ax.set_xlabel(labels[x_axis_index])
    ax.set_ylabel(labels[y_axis_index])

    if save_file is None:
        plt.show()
    else:
        plt.savefig(save_file)

if __name__ == "__main__":
    from polynomial_generators import ball_random_qp
    # Use the same generator, but instead but instead of plotting the roots,
    # just plot all of the coefficients (concatenate all of the lists)
    plot_2D(sum(ball_random_qp(degree=2, number=500, radius=10), []))
