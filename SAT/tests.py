# Testing file

"""
Old dpll function

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