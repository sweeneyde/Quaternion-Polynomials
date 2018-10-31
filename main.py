from quat_poly import quat_poly
from polynomial_generators import *
from quat_plotter import plot
import csv
from time import time
from multiprocessing import Process, Manager, Pool

########## Choose which polynomials ################################

polynomial_generator = all_signs_qp(degree=3)

########## Solve them ##############################################
#
# def processCoefs(coefs, individual_solutions, class_solutions):
#     inds, cls = quat_poly(*coefs, 1).roots()
#     individual_solutions += inds
#     class_solutions += cls

def main():
    ########## Solve ##################################################

    individual_solutions = []
    class_solutions= []
    for coefs in polynomial_generator:
        inds, cls = quat_poly(*coefs, 1).roots()
        individual_solutions += inds
        class_solutions += cls

    # start_time = time()
    #
    # with Manager() as manager:
    #     class_solutions = manager.list()
    #     individual_solutions = manager.list()
    #
    #     processes = []
    #     for i, coefs in enumerate(polynomial_generator):
    #         #print(i)
    #         p = Process(target=processCoefs,
    #                     args=(coefs, individual_solutions, class_solutions)
    #                     )
    #         processes.append(p)
    #         p.start()
    #         if len(processes)>100:
    #             # print('d', i)
    #             processes[0].join()
    #             del processes[0]
    #
    #     map(lambda p:p.join(), processes)
    # #
    # with Pool(processes=10) as pool:
    #     class_solutions = []
    #     individual_solutions = []
    #     pool.map(processCoefs, zip(polynomial_generator), class_solutions, individual_solutions)

    #print(f"Total run time: {time()-start_time} seconds")

    ########## Save and Print the solutions ###########################

    print("Root Classes:")
    for rep in class_solutions:
        if rep: print(rep)

    with open(f"{int(time())}_solns.txt", 'w', newline='') as file:
        out = csv.writer(file, delimiter=',')
        for a,b,c,d in individual_solutions:
            out.writerow((a,b,c,d))

    ########## Plot the solutions ######################################

    plot([(a,b,c,d) for a,b,c,d in individual_solutions])


if(__name__=="__main__"):
    main()
