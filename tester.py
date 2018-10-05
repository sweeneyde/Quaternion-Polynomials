from quat_poly import quat_poly
from quat_random_generators import *
from quat_plotter import plot
import csv
import time

########## Choose which polynomials ################################

polynomial_generator = all_signs_qp(degree=4)

########## Solve them ##############################################

individual_solutions = []

for coefficients in polynomial_generator:
    # Construct a monic quaternion polynomial:
    p = quat_poly(*coefficients, 1)
    inds, cls = p.roots()
    individual_solutions += inds

with open(str(int(time.time()))+"_solns.txt", 'w', newline='') as file:
    out = csv.writer(file, delimiter=',')
    for a,b,c,d in individual_solutions:
        out.writerow((a,b,c,d))

########## Plot the solutions ######################################

#plot([(b,c,d,a) for a,b,c,d in individual_solutions])
