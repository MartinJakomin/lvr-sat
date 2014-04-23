__author__ = 'Martin Jakomin & Mateja Rojko'

from n1 import *
from n2 import *


def get_literals_dict(f):
    """
    Gets dictionary of all literals with information about their purity and independence
    """

    s = []
    ind = []
    r = {}

    # If f is literal return it
    if isinstance(f, Var):
        r[f.name] = 1
        return r
    elif isinstance(f, Neg):
        r[f.value.name] = -1
        return r

    # Fllatens the list
    for x in f.value:
        if isinstance(x, Or) or isinstance(x, And):
            s.extend(x.value)
        else:
            s.append(x)
            ind.append(x)
    # Purity check
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
    # Independent variables
    for x in ind:
        if isinstance(x, Var):
            r[x.name] = 1
        elif isinstance(x, Neg):
            r[x.value.name] = -1
    return r


def dpll(f,v):
    """
    Advanced DPLL algorithm, with while loop simplification and clause length sorting
    """

    f = cnf(f)

    # If f is simplified to a constant
    if isinstance(f,Const):
        if f.value is True:
            return True, v
        else:
            return False, {}

    # While loop simplify
    xs = get_literals_dict(f)
    i = 0
    while 1 in xs.values() or -1 in xs.values():

        # Deleting of pure literals
        for x in xs.keys():
            if xs[x] is 1:
                v[x] = True
            elif xs[x] is -1:
                v[x] = False
        f = solve_cnf(f, v)

        # If f is simplified to a constant
        if isinstance(f,Const):
            if f.value is True:
                return True, v
            else:
                return False, {}
        xs = get_literals_dict(f)
        i += 1


    # Clauses sorted by length
    f2 = sorted(f.value, key=lambda x: x.length())
    first = f2[0]
    first = first.value[0]
    # Get the name of first literal in shortest clause
    if isinstance(first, Var):
        first = first.name
    else:
        first = first.value.name

    # Safe copy of dictionary
    v2 = v.copy()

    #print
    #print f.length(), len(v), len(f.value)
    #print

    # Case true
    v[first] = True
    ft = solve_cnf(f, v)
    rec = dpll(ft,v)
    if rec[0]:
        return rec
    # Case false
    else:
        v2[first] = False
        ff = solve_cnf(f, v2)
        rec2 = dpll(ff,v2)
        return rec2







# Examples


f = And([Var("n"),Var("d"),Or([Var("p"),And([Var("s"),Var("m"),Var("k"),Or([Var("l"),Var("r"),Var("n")])]),Var("u"),Neg(Var("s1")),Var("k"),And([Neg(Var("s")),Neg(Var("k"))])])])

V = ["v1","v2","v3","v4"]
E = {
    "v1v2": 1,
    "v1v3": 0,
    "v2v3": 1,
    "v1v4": 1
}
f = graph2SAT(V,E,2)

"""
v = [[random.randint(1,9) if random.random() > 0.96 else "" for x in range(9)] for y in range(9)]
for i in v:
    print i
print

f = sudoku2SAT(v)
"""

print
print f
print cnf(f)
print
print dpll(f,{})

