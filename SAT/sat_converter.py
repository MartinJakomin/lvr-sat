__author__ = "Martin Jakomin, Mateja Rojko"


"""
Conversion of multiple problems to Boolean expressions (for SAT solving):
- n-coloring of a graph
- Sudoku
"""


from collections import defaultdict
from bool import Var, Neg, And, Or

# functions

def graph2SAT(V, E, n):
    """
    n-coloring of a graph G=(V,E)

    Example Graph:
    V = ["v1","v2","v3","v4"]
    E = {
        "v1v2": 1,
        "v1v3": 0,
        "v2v3": 1,
        "v1v4": 1
    }
    f = graph2SAT(V,E,2)
    """

    f = And([Or([Var("C"+str(i)+","+str(j)) for j in range(1, n+1)]) for i in range(1, len(V)+1)])
    s = []
    for i in range(1, len(V)+1):
        for k in range(1, n+1):
            for l in range(k+1, n+1):
                s.append(Neg(And([Var("C"+str(i)+","+str(k)), Var("C"+str(i)+","+str(l))])))
    f.value.extend(s)
    f = And(f.value)
    s = []
    for v1 in E.keys():
        if E[v1] is 1:
            v = v1.split("v")
            i = v[1]
            j = v[2]
            for k in range(1, n+1):
                s.append(Neg(And([Var("C"+str(i)+","+str(k)), Var("C"+str(j)+","+str(k))])))
    f.value.extend(s)
    f = And(f.value)
    return f


def sudoku2SAT(v):
    """
    Sudoku

    Example Sudoku:
    v = [[random.randint(1,9) if random.random() > 0.6 else "" for x in range(9)] for y in range(9)]
    f = sudoku2SAT(v)
    """

    # Graph of adjacent fields
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
        if 0 < i % 27 < 10:
            for j in (1, 2):
                for k in range(3):
                    if i % 3 is 1:
                        E["v"+str(i)+"v"+str(i+j*9+k)] = 1
                    elif i % 3 is 2:
                        E["v"+str(i)+"v"+str(i-1+j*9+k)] = 1
                    else:
                        E["v"+str(i)+"v"+str(i-2+j*9+k)] = 1

        elif 9 < i % 27 < 19:
            for k in range(3):
                if i % 3 is 1:
                    E["v"+str(i)+"v"+str(i+9+k)] = 1
                elif i % 3 is 2:
                    E["v"+str(i)+"v"+str(i-1+9+k)] = 1
                else:
                    E["v"+str(i)+"v"+str(i-2+9+k)] = 1

    # Starting numbers
    stnum = []
    for j, i in enumerate(reduce(lambda x, y: x+y, v)):
        if i != "":
            stnum.append(Var("C"+str(j+1)+","+str(i)))

    return And([graph2SAT(V, E, 9), And(stnum)])

# no classes
