from quat_poly import quat_poly
from itertools import product

degree = 3

individual_solutions = []
solution_classes = []

for coefficients in product((-1,0,1), repeat=degree):
    # Construct a monic quaternion polynomial:
    p = quat_poly(coefficients+(1,))

    inds, cls = p.roots()
    individual_solutions += inds
    solution_classes += cls

print(max(solution_classes))