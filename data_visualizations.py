import csv
import matplotlib.pyplot as plt
from quat_plotter import plot
from quat_plotter_2D import plot_2D

def load_from_csv(filename):
    global solutions
    with open(filename, 'r') as f:
        solutions = [tuple(float(a) for a in row) for row in csv.reader(f)]

def plot_p_norm(p=2, bins=500):
    """Plot a histogram of the p-norms of the solutions"""
    plt.title(f"{p}-norms of solutions for lattice point quaternion polynomials")
    plt.hist([sum(abs(x)**p for x in abcd)**(1/p) for abcd in solutions], bins=bins)

def plot_imag_p_norm(p=2, bins=500):
    """Plot a histogram of the p-norms of the imaginary parts of the solutions"""
    plt.title(f"{p}-norms of imaginary parts of solutions to polynomials with quaternion coefficients")
    plt.hist([sum(abs(x) ** p for x in abcd[1:]) ** (1 / p) for abcd in solutions], bins=bins)


if __name__=="__main__":
    # # Chose a file:
    load_from_csv('degree_2_individual_roots.csv')

    # # Choose something to plot:
    plot(solutions)
    # plot_2D(solutions, x_axis_index=1, y_axis_index=2, color_axis_index=3)
    # plot_imag_p_norm()
    # plot_p_norm()

    plt.show()

    # # The following can be used to get cross-section images of the solutions.
    # n = 50
    # for i in range(int(-2.5*n), int(2.5*n)+1):
    #     print(i)
    #     imin, imax = i/n, (i+1)/n
    #     L = [q for q in solutions if imin<=q[3]<imax]
    #     if L:
    #         plot_2D(L, save_file=f'degree 2 slices/d3_slice_{i+int(2.5*n)}_{i}', max_scale=2.5, title=f'k={imin}')
    #         plt.close()