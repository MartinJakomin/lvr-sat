__author__ = "Martin Jakomin, Mateja Rojko"


"""
SAT solver based on DPLL algorithm

Functions:
- get_literals
- sat
"""

from bool import Var, Neg, And, Or, Const, cnf, simplify_cnf

# functions


def get_literals(f):
    """
    Gets a dictionary of all literals with information about their purity and independence
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

    # Flattens the list
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


def sat(f, v):
    """
    Improved DPLL algorithm, with while loop simplification and clause length sorting
    Returns True and a list of variable settings if f is satisfiable, else it returns False and empty dictionary

    Example call:
    sat(And([Var("p"), Neg(Var("p"))]), {})
    or you can set initial variables:
    sat(And([Var("p"), Neg(Var("p"))]), {"p": False})
    """

    # If v is not empty, first simplify the function
    if v:
        f = simplify_cnf(f, v)
    else:
        f = cnf(f)

    # If f is simplified to a constant
    if isinstance(f, Const):
        if f.value is True:
            return True, v
        else:
            return False, {}

    # While loop simplify
    xs = get_literals(f)
    i = 0
    while 1 in xs.values() or -1 in xs.values():
        # Deleting of pure literals
        for x in xs.keys():
            if xs[x] is 1:
                v[x] = True
            elif xs[x] is -1:
                v[x] = False
        f = simplify_cnf(f, v)
        # If f is simplified to a constant
        if isinstance(f, Const):
            if f.value is True:
                return True, v
            else:
                return False, {}
        xs = get_literals(f)
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

    # Case true
    v[first] = True
    ft = simplify_cnf(f, v)
    rec = sat(ft, v)
    if rec[0]:
        return rec
    # Case false
    else:
        v2[first] = False
        ff = simplify_cnf(f, v2)
        rec2 = sat(ff, v2)
        return rec2


# no classes
