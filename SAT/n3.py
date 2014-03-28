__author__ = 'Martin Jakomin & Mateja Rojko'

from n1 import *



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
    v = {}
    xs = []

    # If f is simplified to a constant
    if isinstance(f,Const):
        if f.value is True:
            return True, v
        else:
            return False


    cs = f.value


    while len(cs) > 1:
        print "......"
        print cs

        xs = get_literals_dict(f)
        # Deleting of pure literals
        for x in xs.keys():
            if xs[x] is 1:
                v[x] = True
            elif xs[x] is -1:
                v[x] = False


        print "."
        print f
        f = f.solve_cnf(v)
        print f
        f = f.simplify()
        print f
        print


        # if we have no more free variables to set
        if len(xs) < 1:
            return False

        # If f is simplified to a constant
        if isinstance(f,Const):
            if f.value is True:
                return True, v
            else:
                return False

        print "....."
        print f
        cs = f.value

    return True, v






f = And([Var("n"),Var("d"),Or([Var("p"),And([Var("s"),Var("m"),Var("k"),Or([Var("l"),Var("r"),Var("n")])]),Var("u"),Neg(Var("s1")),Var("k"),And([Neg(Var("s")),Neg(Var("k"))])])])
f = Or([And([Var("p"),Neg(Var("q"))]),And([Var("r"),Var("s")]),And([Var("q"),Var("r"),Neg(Var("s"))])])
f = Or([And([Var("p"),Neg(Var("q"))]),And([Var("r"),Var("s")])])


print f
print cnf(f)
print dpll(f)

