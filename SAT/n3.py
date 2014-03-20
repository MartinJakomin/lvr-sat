__author__ = 'Martin Jakomin & Mateja Rojko'

from n1 import *


def cnf(f):
    return nnf(f).cnf().simplify()


print cnf(Or([Var("p"),And([Var("s"),Var("m"),Var("k"),Or([Var("l"),Var("r"),Var("n")])]),Var("u")]))
print
print cnf(Or([And([Var("p"),Neg(Var("q"))]),And([Var("r"),Var("s")]),And([Var("q"),Var("r"),Neg(Var("s"))])]))