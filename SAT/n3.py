__author__ = 'Martin Jakomin & Mateja Rojko'

from n1 import *


def cnf(f):
    print f
    return nnf(f).cnf()


f = Neg(And([Var("p"),And([Var("p"),Var("p"),Var("q"),Var("p"),Neg(Var("p1")),Const(True)])]))
print f
print simplify(f)
print cnf(f)