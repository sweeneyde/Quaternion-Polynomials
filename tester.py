from quat_poly import quat_poly
from quat_random_generators import *
from quat_plotter import plot

########## Generate ################################################

polynomial_generator = ball_random_qp(degree=2, number=100, radius=10)


########## Solve ###################################################

individual_solutions = [] #set()
# solution_classes = set()
for coefficients in polynomial_generator:
    # Construct a monic quaternion polynomial:
    p = quat_poly(*coefficients, 1)

    inds, cls = p.roots()
    individual_solutions += inds
#    solution_classes |= set(cls)


########## Plot ####################################################

plot(individual_solutions)
#plot( sum(disk_random_qp(degree=2, number=100, radius =10), []) )