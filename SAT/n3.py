__author__ = 'Martin Jakomin & Mateja Rojko'

from n1 import *
from n2 import *



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


"""
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


    while len(cs) > 0:
        print "......", len(cs), "......."
        print f

        xs = get_literals_dict(f)
        print xs
        # Deleting of pure literals
        for x in xs.keys():
            if xs[x] is 1:
                v[x] = True
            elif xs[x] is -1:
                v[x] = False

        f = f.solve_cnf(v)
        f = cnf(f)

        # If f is simplified to a constant
        if isinstance(f,Const):
            if f.value is True:
                return True, v
            else:
                return False

        cs = f.value

        # if we have no more free variables to set
        if len(xs) < 1:
            return False

        #TODO: Set variable ...

        v[xs.keys()[0]] = True


    return True, v
"""


#TODO: Do Recursive
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


    while len(cs) > 0:
        print "......", len(cs), "......."
        print f

        xs = get_literals_dict(f)
        print xs
        # Deleting of pure literals
        for x in xs.keys():
            if xs[x] is 1:
                v[x] = True
            elif xs[x] is -1:
                v[x] = False

        f = f.solve_cnf(v)
        f = cnf(f)

        # If f is simplified to a constant
        if isinstance(f,Const):
            if f.value is True:
                return True, v
            else:
                return False

        cs = f.value

        # if we have no more free variables to set
        if len(xs) < 1:
            return False

        #TODO: Set variable ...

        v[xs.keys()[0]] = True


    return True, v






#f = And([Var("n"),Var("d"),Or([Var("p"),And([Var("s"),Var("m"),Var("k"),Or([Var("l"),Var("r"),Var("n")])]),Var("u"),Neg(Var("s1")),Var("k"),And([Neg(Var("s")),Neg(Var("k"))])])])
#f = Or([And([Var("p"),Neg(Var("q"))]),And([Var("r"),Var("s")]),And([Var("q"),Var("r"),Neg(Var("s"))])])
#f = Or([And([Var("p"),Neg(Var("q"))]),And([Var("r"),Var("s")])])
#f = And([Var("q"),Var("p"),Or([Neg(Var("q")),Var("p"),Neg(Var("p"))])])



V = ["v1","v2","v3","v4"]
E = {
    "v1v2": 1,
    "v1v3": 0,
    "v2v3": 1,
    "v1v4": 1
}
f = graph2SAT(V,E,2)

print f
print cnf(f)
print
print dpll(f)

