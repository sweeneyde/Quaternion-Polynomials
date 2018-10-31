from quat_poly import quat_poly
from polynomial_generators import *
from quat_plotter import plot
import csv
from time import time

########## Choose which polynomials ################################

polynomial_generator = all_signs_qp(degree=3)

def main():
    ########## Solve ##################################################

    start_time = time()

    individual_solutions = []
    class_solutions= []
    for coefs in polynomial_generator:
        inds, cls = quat_poly(*coefs, 1).roots()
        individual_solutions += inds
        class_solutions += cls

    print(f"Total run time: {time()-start_time} seconds")

    ########## Save and Print the solutions ###########################

    print("Root Classes:")
    for rep in class_solutions:
        if rep: print(rep)

    with open(f"{int(time())}_solns.txt", 'w', newline='') as file:
        out = csv.writer(file, delimiter=',')
        for a,b,c,d in individual_solutions:
            out.writerow((a,b,c,d))

    ########## Plot the solutions ######################################

    # Here we can change which component gets represented as color
    plot([(a,b,c,d) for a,b,c,d in individual_solutions])


if(__name__=="__main__"):
    main()
