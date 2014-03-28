__author__ = 'Martin Jakomin & Mateja Rojko'

import random
from collections import defaultdict
from n1 import *


def Graph2SAT(V,E,n):
    """
    n-coloring of a graph G=(V,E)
    """

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


def Sudoku2SAT():
    """
    Sudoku
    """

    V = ["v"+str(i) for i in range(1, 82)]
    E = defaultdict(int)
    for i in range(9):
        for j in range(1, 10):
            for k in range(j+1, 10):
                E["v"+str(j+(i*9))+"v"+str(k+(i*9))] = 1

    for i in range(9):
        for j in range(1, 10):
            for k in range(1, 9-i):
                E["v"+str(j+(i*9))+"v"+str(j+k*9+(i*9))] = 1

    for i in range(1, 82):
        if i%27 < 10 and i%27 >0:
            for j in (1, 2):
                for k in range(3):
                    if i%3 is 1:
                        E["v"+str(i)+"v"+str(i+j*9+k)] = 1
                    elif i%3 is 2:
                        E["v"+str(i)+"v"+str(i-1+j*9+k)] = 1
                    else:
                        E["v"+str(i)+"v"+str(i-2+j*9+k)] = 1

        elif i%27 > 9 and i%27 < 19:
            for k in range(3):
                if i%3 is 1:
                    E["v"+str(i)+"v"+str(i+9+k)] = 1
                elif i%3 is 2:
                    E["v"+str(i)+"v"+str(i-1+9+k)] = 1
                else:
                    E["v"+str(i)+"v"+str(i-2+9+k)] = 1

    print (sorted(E))
    print (len(E))

    f = Graph2SAT(V,E,9)
    #TODO: Dodaj vrednosti
    return f


#Example sudoku
#v = [[random.randint(1,9) if random.random() > 0.6 else "" for x in range(9)] for y in range(9)]
#print()
#for i in v:
#    print (i)
#print()
#print()
#print (Sudoku2SAT(v))
Sudoku2SAT()
