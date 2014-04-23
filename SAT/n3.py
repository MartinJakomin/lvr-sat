__author__ = 'Martin Jakomin & Mateja Rojko'

from n1 import *
from n2 import *


def get_literals_dict(f):
    s = []
    ind = []
    for x in f.value:
        if isinstance(x, Or) or isinstance(x, And):
            s.extend(x.value)
        else:
            s.append(x)
            print x
            ind.append(x)
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

    # Independent variables
    for x in ind:
        if isinstance(x, Var):
            r[x.name] = 1
        elif isinstance(x, Neg):
            r[x.value.name] = -1
        else:
            r[x.name] = 0

    return r


def dpll(f,v):
    f = cnf(f)
    print "..."

    

    #TODO: Simplify in while loop
    i = 0
    xs = get_literals_dict(f)
    print xs
    while 1 in xs.values() or -1 in xs.values():
        # If f is simplified to a constant
        if isinstance(f,Const):
            if f.value is True:
                return True, v
            else:
                return False, {}

        #xs = get_literals_dict(f)
        print "---"+ str(i)
        print xs
        #cs = f.value

        # Deleting of pure literals
        for x in xs.keys():
            if xs[x] is 1:
                v[x] = True
            elif xs[x] is -1:
                v[x] = False

        f = solve_cnf(f, v)
        xs = get_literals_dict(f)
        i += 1
        #f = cnf(f)




    print len(v)
    print

    # If f is simplified to a constant
    if isinstance(f,Const):
        if f.value is True:
            return True, v
        else:
            return False, {}


    print v





    #TODO: Sort clauses by length, shorter first...

    f2 = sorted(f.value, key=lambda x: x.length())
    first = f2[0]
    first = first.value[0]
    #TODO: take -1 or +1 for neg and var ...., Also bug: enojni literali v OR-u !!!


    xs = get_literals_dict(f)
    print "..,.,.,.,.,.,,"
    print f
    print f2
    print And(f2)
    print xs
    print "chosen old: " + str(xs.keys()[0]) + " chosen new: " + str(first)
    print "..,.,.,.,.,.,,"



    # Safe copy of dictionary
    v2 = v.copy()

    #case true
    v[xs.keys()[0]] = True
    f = solve_cnf(f, v)
    rec = dpll(f,v)
    if rec[0]:
        return rec
    # case false
    else:
        v2[xs.keys()[0]] = False
        f = solve_cnf(f, v2)
        rec2 = dpll(f,v2)
        return rec2


#f = And([Var("n"),Var("d"),Or([Var("p"),And([Var("s"),Var("m"),Var("k"),Or([Var("l"),Var("r"),Var("n")])]),Var("u"),Neg(Var("s1")),Var("k"),And([Neg(Var("s")),Neg(Var("k"))])])])
#f = Or([And([Var("p"),Neg(Var("q"))]),And([Var("r"),Var("s")]),And([Var("q"),Var("r"),Neg(Var("s"))])])
#f = Or([And([Var("p"),Neg(Var("q"))]),And([Var("r"),Var("s")])])
f = And([Var("q"),Var("p"),Or([Neg(Var("q")),Var("p"),Neg(Var("p"))])])



V = ["v1","v2","v3","v4"]
E = {
    "v1v2": 1,
    "v1v3": 0,
    "v2v3": 1,
    "v1v4": 1
}
f = graph2SAT(V,E,2)


"""
v = [[random.randint(1,9) if random.random() > 0.1 else "" for x in range(9)] for y in range(9)]
for i in v:
    print i
print

f = sudoku2SAT(v)
"""


print f
print f.length()
print [x.length() for x in cnf(f).value]

print len(get_literals_dict(cnf(f)))
print cnf(f)
print
print dpll(f,{})

