import csv
import matplotlib.pyplot as plt
from quat_plotter import plot
from quat_plotter_2D import plot_2D
from pyquaternion import Quaternion as Q
from numpy import histogram

def load_from_csv(filename):
    global solutions
    with open(filename, 'r') as f:
        solutions = [tuple(float(a) for a in row) for row in csv.reader(f)]

def plot_p_norm(p=2, bins=500):
    plt.title(f"{p}-norms of solutions for lattice point quaternion polynomials")
    plt.hist([sum(abs(x)**p for x in abcd)**(1/p) for abcd in solutions], bins=bins)

def plot_imag_p_norm(p=2, bins=500):
    plt.title(f"{p}-norms of imaginary parts of solutions to polynomials with quaternion coefficients")
    plt.hist([sum(abs(x) ** p for x in abcd[1:]) ** (1 / p) for abcd in solutions], bins=bins)

if __name__=="__main__":
    load_from_csv('degree_3_signs_solutions.txt')
    # plot(solutions)
    # plot_2D(solutions, x_axis_index=1, y_axis_index=2, color_axis_index=3)
    # plot_imag_p_norm()
    # plot_p_norm()