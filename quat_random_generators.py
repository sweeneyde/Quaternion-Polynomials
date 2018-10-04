from random import uniform, gauss
import math
from pyquaternion import Quaternion as Q
from itertools import product

def all_signs_qp(degree):
    all_quats = product((-1, 0, 1), repeat=4)
    for coords in product(all_quats, repeat=degree):
        yield [Q(a) for a in coords]

def uniform_random_qp(degree, smallest, biggest, number):
    r = lambda: uniform(smallest, biggest)
    for _ in range(number):
        yield [Q(r(), r(), r(), r()) for _ in range(degree)]


def gaussian_random_qp(degree, number):
    r = lambda: gauss(0, 10)
    for _ in range(number):
        yield [Q(r(), r(), r(), r()) for _ in range(degree)]

def ball_random_qp(degree, number, radius=1):
    def on_ball():
        r = lambda: uniform(-1, 1)
        q = Q(r(), r(), r(), r())
        while not (q.norm <= 1):
            q = Q(r(), r(), r(), r())
        return q
    for _ in range(number):
        yield [on_ball()*radius for _ in range(degree)]

def disk_random_qp(degree, number, radius=1):
    r = lambda: uniform(0, 2*math.pi)
    def on_disk():
        t = r()
        ab_weight, cd_weight = math.cos(t), math.sin(t)
        t1 = r()
        a, b = ab_weight * math.cos(t1), ab_weight * math.sin(t1)
        t2 = r()
        c, d = cd_weight * math.cos(t2), cd_weight * math.sin(t2)
        return Q(a,b,c,d)
    for _ in range(number):
        yield [on_disk()*radius for _ in range(degree)]


if __name__ == "__main__":
    print('\n'.join(str(x) for x in all_signs_qp(2)))
