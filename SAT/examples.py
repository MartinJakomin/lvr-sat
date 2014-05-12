__author__ = "Martin Jakomin, Mateja Rojko"

from bool import Var, Neg, And, Or, Const, cnf, simplify_cnf, nnf, simplify, solve
from sat import sat, get_literals
from sat_converter import sudoku2SAT, graph2SAT

### Operators ###
print "OPERATORS"
print "~~~~~~~~~"

# Const
tr = Const(True)
fl = Const(False)
print "Constants:", tr, ",", fl

# Var
op = Var("p")
print "Variable:", op

# Neg
n = Neg("p")
print "Negation:", n

# And
a1 = And([Var("p"), Var("q")])
a2 = And([Var("p"), Var("q"), Var("r")])
a3 = And([Var("p"), And([Var("q"), Neg(Var("r"))])])
print "Conjunction:", a1, ", ", a2, ", ", a3

# Or
o1 = Or([Var("p"), Var("q")])
o2 = Or([Var("p"), Var("q"), Var("r")])
o3 = Or([Var("p"), Or([Var("q"), Var("r")])])
print "Disjunction:", o1, ", ", o2, ", ", o3, "\n\n"


### Functions ###
print "FUNCTIONS"
print "~~~~~~~~~"

# nnf
nnf1 = nnf(Neg(Neg(Var("p"))))
nnf2 = nnf(Neg(Or([Var("p"), Var("q")])))
nnf3 = nnf(Neg(Or([Const(True), Var("p")])))
print "Negation normal form:", nnf1, ", ", nnf2, ", ", nnf3

# cnf
cnf1 = cnf(Or([And([Var("p"), Var("q")]), Var("r")]))
cnf2 = cnf(Neg(Or([Var("p"), Var("q")])))
cnf3 = cnf(And([Var("p"), Or([Var("q"), And([Var("r"), Var("z")])])]))
print "Conjunctive normal form:", cnf1, ", ", cnf2, ", ", cnf3

# simplify
sim1 = simplify(Or([Const(True), Const(True)]))
sim2 = simplify(Or([Const(True), Var("p")]))
sim3 = simplify(And([Const(False), Var("p")]))
sim4 = simplify(Neg(And([Neg(Or([Neg(Var("p")), Var("q")])), Neg(And([Var("q"), Const(False)]))])))
sim5 = simplify(Or([Var("p"), Neg(Var("p"))]))
sim6 = simplify(And([Var("p"), Var("p"), Var("q")]))
sim7 = simplify(And([Var("p"), Var("p"), Var("q"), Const(False)]))
print "Simplify:", sim1, ", ", sim2, ", ", sim3, ", ", sim4, ", ", sim5, ", ", sim6, ", ", sim7

# SAT
sat1 = sat(And([Var("p"), Var("q")]), {})
sat2 = sat(Neg(Or([Const(True), Const(False)])), {})
print "SAT:", sat1, ", ", sat2

# SAT - set initial values
sat3 = sat(And([Or([Var("p"), Var("q")]), And([Var("p"), Neg(Var("q"))]), Var("s")]), {"p": False})
print "SAT - set initial values:", sat1, ", ", sat2, "\n\n"


### SUDOKU ###
print "SUDOKU"
print "~~~~~~~~~"

sudoku = [[2, 1, "", 3, "", "", 4, "", ""],
          ["", "", "", 4, 6, "", "", "", 5],
          ["", "", "", "", "", 5, 7, "", ""],
          ["", 9, "", "", "", "", "", 2, ""],
          [8, "", "", "", "", "", "", "", ""],
          ["", 3, "", "", 8, "", "", 9, 1],
          [6, 2, "", "", "", 9, "", "", ""],
          ["", "", 9, 6, "", "", 8, "", ""],
          ["", "", "", 7, 3, "", "", 5, ""]]
print "Sudoku:", sat(sudoku2SAT(sudoku), {}), "\n\n"


### graph coloring ###
print "GRAPH COLORING"
print "~~~~~~~~~"

# cyclic graph on odd number of points
V1 = ["v1", "v2", "v3"]
E1 = {"v1v2": 1, "v2v3": 1, "v3v1": 1}
print "Cyclic graph on odd number of points:", sat(graph2SAT(V1,E1,3), {})

# cyclic graph on even number of points
V2 = ["v1", "v2", "v3", "v4"]
E2 = {"v1v2": 1, "v2v3": 1, "v3v4": 1, "v4v1": 1}
print "Cyclic graph on even number of points:", sat(graph2SAT(V2,E2,2), {})

# bipartite graph
V3 = ["v1", "v2", "v3", "v4"]
E3 = {"v1v3": 1, "v1v4": 1, "v2v4": 1}
print "Bipartite graph:", sat(graph2SAT(V3,E3,2), {})

# complete graph
V4 = ["v1", "v2", "v3", "v4"]
E4 = {"v1v2": 1, "v1v3": 1, "v1v4": 1, "v2v3": 1, "v2v4": 1, "v3v4": 1}
print "Complete graph:", sat(graph2SAT(V4,E4,4), {})

# tree
V5 = ["v1", "v2", "v3", "v4", "v5"]
E5 = {"v1v2": 1, "v1v3": 1, "v3v4": 1, "v3v5": 1}
print "Tree:", sat(graph2SAT(V5,E5,2), {})

# Petersen graph
V6 = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10"]
E6 = {"v1v2": 1, "v1v5": 1, "v1v6": 1, "v2v3": 1, "v2v7": 1, "v3v4": 1, "v3v8": 1, "v4v5": 1, "v4v9": 1, "v5v10": 1, "v6v8": 1, "v6v9": 1, "v7v9": 1, "v7v10": 1, "v8v10": 1}
print "Petersen graph:", sat(graph2SAT(V6,E6,3), {})