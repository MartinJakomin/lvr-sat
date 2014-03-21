__author__ = 'Martin Jakomin & Mateja Rojko'

from n1 import *


def cnf(f):
    return nnf(f).cnf().simplify()


#print cnf(Or([Var("p"),And([Var("s"),Var("m"),Var("k"),Or([Var("l"),Var("r"),Var("n")])]),Var("u")]))
#print cnf(Or([And([Var("p"),Neg(Var("q"))]),And([Var("r"),Var("s")]),And([Var("q"),Var("r"),Neg(Var("s"))])]))
#print


"""
def get_literals(lst):
    r = set()
    for x in lst:
        if isinstance(x,Var):
            r.add(x.name)
        elif isinstance(x,Neg):
            r.add(x.value.name)
        else:
            r = r.union(get_literals(x.value))
    return r
"""


def get_literals_dict(f):
    s = []
    for x in f.value:
        if isinstance(x, Or) or isinstance(x, And):
            s.extend(x.value)
        else:
            s.append(x)
    r = {}
    for x in s:
        if isinstance(x, Var):
            if x.name in r and r[x.name] is not 1:
                r[x.name] = 0
            else:
                r[x.name] = 1
        elif isinstance(x, Neg):
            if x.value.name in r and r[x.value.name] is not -1:
                r[x.value.name] = 0
            else:
                r[x.value.name] = -1
    return r


def dpll(f):
    f = cnf(f)
    cs = f.value
    xs = get_literals_dict(f)
    v = {}
    print xs
    print cs
    print "----"

    #TODO: while cs has any, what about cs = Const ??
    for i in range(1):

        xs = get_literals_dict(f) # ??
        # Deleting of pure literals
        for x in xs.keys():
            if xs[x] is 1:
                v[x] = True
            elif xs[x] is -1:
                v[x[1:]] = False

        print f
        print v

        f = f.solve_cnf(v)
        print f
        f = f.simplify()
        print f, f.__class__
        print



        if len(xs) < 1:
            return False

    return True, v






f = Or([Var("p"),And([Var("s"),Var("m"),Var("k"),Or([Var("l"),Var("r"),Var("n")])]),Var("u")])
f2 = Or([And([Var("p"),Neg(Var("q"))]),And([Var("r"),Var("s")]),And([Var("q"),Var("r"),Neg(Var("s"))])])

#dpll(f)
dpll(f2)

"""
f2 = cnf(f2)
print
print f2
f3 = f2.solve_cnf({"p":True, "q1": False})
print
print f3
print
print "-------"
print f3
print
print simplify(f3)
"""
