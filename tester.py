from quat_poly import quat_poly
from quat_random_generators import *
from quat_plotter import plot

########## Choose which polynomials ################################

polynomial_generator = all_signs_qp(degree=3)

########## Solve them ##############################################

individual_solutions = []

for coefficients in polynomial_generator:
    # Construct a monic quaternion polynomial:
    p = quat_poly(*coefficients, 1)
    inds, cls = p.roots()
    individual_solutions += inds

########## Plot the solutions ######################################

plot(individual_solutions)
