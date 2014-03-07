__author__ = 'Martin Jakomin'

import random
from collections import defaultdict
from n1 import *

#Barvanje grafa
def Graph2SAT(V,E,n):
    f = And([Or([Var("C"+str(i)+","+str(j)) for j in range(1,n+1)]) for i in range(1,len(V)+1)])
    s = []
    for i in range(1,len(V)+1):
        for k in range(1,n+1):
            for l in range(k+1,n+1):
                s.append(Neg(And([Var("C"+str(i)+","+str(k)),Var("C"+str(i)+","+str(l))])))
    f.value.extend(s)
    f = And(f.value)
    s = []
    for v1 in E.keys():
        if E[v1] is 1:
            v = v1.split("v")
            i = v[1]
            j = v[2]
            s1 = []
            for k in range(1,n+1):
                s1.append(And([Var("C"+str(i)+","+str(k)),Var("C"+str(j)+","+str(k))]))
            s.append(Neg(And(s1)))
    f.value.extend(s)
    f = And(f.value)
    return f


#Sudoku
def Sudoku2SAT(v):

    V = ["v"+str(i) for i in range(1, 82)]
    E = defaultdict(int)

    #E[kljuc] = vrednost
    for i in range(9):
        for j in range(1, 10):
            for k in range(j+1, 10):
                E["v"+str(j+(i*9))+"v"+str(k+(i*9))] = 1


    print sorted(E)
    print len(E)


    #TODO: Stolpci in 3x3

    f = Graph2SAT(V,E,9)

    #TODO: Dodaj vrednosti

    return f




V = ["v1","v2","v3"]
E = {
    "v1v2": 1,
    "v1v3": 0,
    "v2v3": 1,
}

print Graph2SAT(V,E,3)

v = [[random.randint(1,9) if random.random() > 0.996 else "" for x in range(9)] for y in range(9)]

print
for i in v:
    print i

print
print
print Sudoku2SAT(v)