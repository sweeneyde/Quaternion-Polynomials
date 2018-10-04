'''
Gets the quaternion roots of a quaternion polynomial.
This algorithm comes from:
[1] R.Serôdio, E.Pereira, and J.Vitória. Computing the zeros of quaternion polynomials.
    http://www.sciencedirect.com/science/article/pii/S0898122101002358
'''
from pyquaternion import Quaternion as Q
from numpy import linalg as LA
from math import sqrt


class quat_poly:
    def __init__(self, *args):
        assert args[-1] == Q(1, 0, 0, 0)
        self.coefficients = [Q(q) for q in args]

    def __call__(self, x):
        return self.eval_at(x)

    def eval_at(self, x):
        '''Evaluate the polynomial at a point'''
        return sum((k * (x ** i) for i, k in enumerate(self.coefficients)), Q(0))

    def companion_matrix(self):
        '''
        Gets the following complex square matrix, consisting of an upper
        off-diagonal of ones and a bottom row of the polynomial coefficients:
        | 0    1    0  ...  0 |
        | 0    0    1  ...  0 |
        | ................... |
        | 0    0    0  ...  1 |
        |-q_0, -q_1 ... -q_m-1|
        :return: The list of lists representing this companion matrix
        '''
        m = len(self.coefficients) - 1
        return \
            [[int(j == i + 1) for j in range(m)]
             for i in range(m - 1)] \
            + [[-q for q in self.coefficients[:-1]]]

    def poly_long_remainder(self, t, n):
        '''
        Long-divides the quaternion polynomial by characteristic
        polynomial (x**2 - tx + n).
        Returns the coefficients of the remainder terms
        '''
        remainder = self.coefficients[:]

        for p in range(len(remainder) - 1, 1, -1):
            # Partial Quotient
            q = remainder[p]  # / 1

            # subtract partial quotient * divisor
            # del remainder[p]
            remainder[p - 1] += t * q
            remainder[p - 2] -= n * q

        f, g = remainder[1], remainder[0]
        return f, g

    def unfiltered_roots(self):
        '''
        Find the roots of the polynomial using the algorithm in [1].
        :return: A list of individual zeros, and a list
         of zeros such that every similar quaternion is also a zero -
         that is, a list of representatives of equivalence classes
        '''
        individual_zeros = []
        class_zeros = []
        for l in right_eigenvalues(self.companion_matrix()):
            l = complex(l)
            t = 2 * l.real
            n = l.imag ** 2 + l.real ** 2
            f, g = self.poly_long_remainder(t, n)
            if Q(f).norm < 0.01:
                class_zeros.append(Q(t / 2, sqrt(n - (t / 2) ** 2), 0, 0))
            else:
                q = Q(-(1/f) * g)
                assert self(q).norm < 0.000001
                individual_zeros.append(Q(-(1/f) * g))

        return individual_zeros, class_zeros

    def roots(self):
        '''
        :return: same as unfiltered roots, but with duplicates removed.
        '''
        individuals, classes = self.unfiltered_roots()
        filtered_individuals = []
        filtered_classes = []

        for q in individuals:
            if not any((p - q).norm < 0.000001 for p in filtered_individuals):
                filtered_individuals.append(q)

        for q in classes:
            if not any((p - q).norm < 0.000001 for p in filtered_classes):
                filtered_classes.append(q)

        return filtered_individuals, filtered_classes


def quat_to_complex(q):
    a, b, c, d = Q(q)
    return complex(a, sqrt(b ** 2 + c ** 2 + d ** 2))


def complex_to_quat(z):
    a, b = z.real, z.imag
    return Q(a, b, 0, 0)


def right_eigenvalues(A):
    '''
    Takes in a quaternion matrix A and outputs its left eigenvalues
    :return: A list of left eigenvalues of A
    '''
    A = [[Q(q) for q in row] for row in A]

    # Decompose each element of A into A_1 + A_2*j
    A_1 = [[complex(a, b) for (a, b, c, d) in row] for row in A]
    A_2 = [[complex(c, d) for (a, b, c, d) in row] for row in A]

    A_2_neg_conj = [[-z.conjugate() for z in row] for row in A_2]
    A_1_conj = [[z.conjugate() for z in row] for row in A_1]

    phi = [row1 + row2 for row1, row2 in zip(A_1, A_2)] \
          + [row1 + row2 for row1, row2 in zip(A_2_neg_conj, A_1_conj)]

    return LA.eigvals(phi)


if __name__ == '__main__':
    # Some test cases from the paper [1]:
    def test1():
        global p
        global zeros
        p = quat_poly(
            Q(-4, 0, 2.9, -2.9),
            Q(0, 0, -1, 0),
            Q(0, 0, 0, 0),
            Q(-7.2, 0, 0, 0),
            Q(0, -1, -1, 0),
            Q(-1.7, 0, 0, 0),
            Q(3, -1, 0, 0),
            Q(0, 0, 2.5, 2.1),
            Q(0, -3.1, 0, -1),
            Q(1, 2, -4, 0),
            1
        )

        zeros = [
            Q(-1.26112, -1.92564, 4.10523, -0.55813),
            Q(0.93019, 0.27871, -0.51178, -0.45249),
            Q(-1.07301, 0.46409, -0.09237, -0.14655),
            Q(1.14205, 0.08057, 0.07784, -0.04811),
            Q(-0.65287, -0.01858, 0.88395, -0.27907),
        ]


    def test2():
        global p
        global zeros
        p = quat_poly(
            Q(-12, 0, 6, 0),
            Q(0, 6, 0, 18),
            Q(-4, 0, 5, 0),
            Q(0, 5, 0, 15),
            Q(3, 0, 1, 0),
            Q(0, 1, 0, 3),
            1
        )

        zeros = [
            Q(0, -1, 0, -2),
            Q(0, 3 ** 0.5, 0, 0),
            Q(0, 2 ** 0.5, 0, 0),
            Q(0, -0.6, 0, -0.8)
        ]


    def test3():
        global p
        global zeros
        p = quat_poly(Q(12), Q(8), Q(5), Q(2), Q(1))

        zeros = [
            Q(0.359281, 1.91107, 0, 0),
            Q(-1.35948, 1.15118, 0, 0)
        ]


    for t in (test1, test2, test3):
        print('\n\n' + t.__name__ + '  ' + '=' * 60 + '\n')
        t()

        print(p)
        print('\nValues at theoretical zeros:')
        for q in zeros:
            print('\t{:>12}\t->\t{}'.format(q, p(q).norm))

        print('\nCompanion matrix:')
        C = p.companion_matrix()
        print('\n'.join(str(row) for row in C))

        print('\nEigenvalues:')
        print(right_eigenvalues(C))

        inds, cls = p.roots()
        print('\nIndividual Roots:')
        for ind in inds:
            print('\t{:>24}\t->\t{}'.format(ind, p(ind).norm))
        print('\nRoot classes:')
        for cl in cls:
            print('\t{:>24}\t->\t{}'.format(cl, p(cl).norm))

    print('\nTests finished.')
