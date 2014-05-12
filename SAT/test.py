_author__ = 'Martin Jakomin, Mateja Rojko'

from bool import Var, Neg, And, Or, Const, cnf, simplify_cnf, nnf, simplify, solve
from sat import sat, get_literals
from sat_converter import sudoku2SAT, graph2SAT

import unittest


class SatTests(unittest.TestCase):
    """
    Unit tests for functions:
    - nnf
    - cnf
    - simplify
    - simplify_cnf
    - solve
    - sat
    """


    def test_nnf(self):
        self.assertEqual(str(nnf(Var("p"))), "p")
        self.assertEqual(str(nnf(Const(True))), "True")
        self.assertEqual(str(nnf(Or([Var("p"), Var("q")]))), "(p | q)")
        self.assertEqual(str(nnf(Or([Var("p"), Var("q"), Var("p")]))), "(p | q | p)")
        self.assertEqual(str(nnf(Or([Or([Var("p"), Var("q")]), Var("p")]))), "((p | q) | p)")
        self.assertEqual(str(nnf(Or([Const(True), Const(False)]))), "(True | False)")
        self.assertEqual(str(nnf(Or([Const(False), Const(False)]))), "(False | False)")
        self.assertEqual(str(nnf(Or([Const(True), Const(True)]))), "(True | True)")
        self.assertEqual(str(nnf(Or([Const(True), Var("p")]))), "(True | p)")
        self.assertEqual(str(nnf(And([Var("p"), Var("q")]))), "(p & q)")
        self.assertEqual(str(nnf(And([Var("p"), Var("q"), Var("p")]))), "(p & q & p)")
        self.assertEqual(str(nnf(And([And([Var("p"), Var("q")]), Var("p")]))), "((p & q) & p)")
        self.assertEqual(str(nnf(And([Const(True), Const(False)]))), "(True & False)")
        self.assertEqual(str(nnf(And([Const(False), Const(False)]))), "(False & False)")
        self.assertEqual(str(nnf(And([Const(True), Const(True)]))), "(True & True)")
        self.assertEqual(str(nnf(And([Const(True), Var("p")]))), "(True & p)")

        self.assertEqual(str(nnf(Neg(Var("p")))), "~p")
        self.assertEqual(str(nnf(Neg(Neg(Var("p"))))), "p")
        self.assertEqual(str(nnf(Neg(Const(True)))), "False")
        self.assertEqual(str(nnf(Neg(Or([Var("p"), Var("q")])))), "(~p & ~q)")
        self.assertEqual(str(nnf(Neg(Or([Var("p"), Var("q"), Var("p")])))), "(~p & ~q & ~p)")
        self.assertEqual(str(nnf(Neg(Or([Or([Var("p"), Var("q")]), Var("p")])))), "((~p & ~q) & ~p)")
        self.assertEqual(str(nnf(Neg(Or([Const(True), Const(False)])))), "(False & True)")
        self.assertEqual(str(nnf(Neg(Or([Const(False), Const(False)])))), "(True & True)")
        self.assertEqual(str(nnf(Neg(Or([Const(True), Const(True)])))), "(False & False)")
        self.assertEqual(str(nnf(Neg(Or([Const(True), Var("p")])))), "(False & ~p)")
        self.assertEqual(str(nnf(Neg(And([Var("p"), Var("q")])))), "(~p | ~q)")
        self.assertEqual(str(nnf(Neg(And([Var("p"), Var("q"), Var("p")])))), "(~p | ~q | ~p)")
        self.assertEqual(str(nnf(Neg(And([And([Var("p"), Var("q")]), Var("p")])))), "((~p | ~q) | ~p)")
        self.assertEqual(str(nnf(Neg(And([Const(True), Const(False)])))), "(False | True)")
        self.assertEqual(str(nnf(Neg(And([Const(False), Const(False)])))), "(True | True)")
        self.assertEqual(str(nnf(Neg(And([Const(True), Const(True)])))), "(False | False)")
        self.assertEqual(str(nnf(Neg(And([Const(True), Var("p")])))), "(False | ~p)")
        self.assertEqual(str(nnf(Neg(And([Neg(Or([Neg(Var("p")), Var("q")])), Neg(And([Var("q"), Const(False)]))])))), "((~p | q) | (q & False))")


    def test_cnf(self):
        self.assertEqual(str(cnf(Var("p"))), "p")
        self.assertEqual(str(cnf(Const(True))), "True")
        self.assertEqual(str(cnf(Or([Var("p"), Var("q")]))), "(p | q)")
        self.assertEqual(str(cnf(Or([Var("p"), Var("q"), Var("p")]))), "(q | p)")
        self.assertEqual(str(cnf(Or([Or([Var("p"), Var("q")]), Var("p")]))), "(q | p)")
        self.assertEqual(str(cnf(Or([Const(True), Const(False)]))), "True")
        self.assertEqual(str(cnf(Or([Const(False), Const(False)]))), "False")
        self.assertEqual(str(cnf(Or([Const(True), Const(True)]))), "True")
        self.assertEqual(str(cnf(Or([Const(True), Var("p")]))), "True")
        self.assertEqual(str(cnf(And([Var("p"), Var("q")]))), "(p & q)")
        self.assertEqual(str(cnf(And([Var("p"), Var("q"), Var("p")]))), "(q & p)")
        self.assertEqual(str(cnf(And([And([Var("p"), Var("q")]), Var("p")]))), "(q & p)")
        self.assertEqual(str(cnf(And([Const(True), Const(False)]))), "False")
        self.assertEqual(str(cnf(And([Const(False), Const(False)]))), "False")
        self.assertEqual(str(cnf(And([Const(True), Const(True)]))), "True")
        self.assertEqual(str(cnf(And([Const(True), Var("p")]))), "p")

        self.assertEqual(str(cnf(Neg(Var("p")))), "~p")
        self.assertEqual(str(cnf(Neg(Neg(Var("p"))))), "p")
        self.assertEqual(str(cnf(Neg(Const(True)))), "False")
        self.assertEqual(str(cnf(Neg(Or([Var("p"), Var("q")])))), "(~p & ~q)")
        self.assertEqual(str(cnf(Neg(Or([Var("p"), Var("q"), Var("p")])))), "(~q & ~p)")
        self.assertEqual(str(cnf(Neg(Or([Or([Var("p"), Var("q")]), Var("p")])))), "(~q & ~p)")
        self.assertEqual(str(cnf(Neg(Or([Const(True), Const(False)])))), "False")
        self.assertEqual(str(cnf(Neg(Or([Const(False), Const(False)])))), "True")
        self.assertEqual(str(cnf(Neg(Or([Const(True), Const(True)])))), "False")
        self.assertEqual(str(cnf(Neg(Or([Const(True), Var("p")])))), "False")
        self.assertEqual(str(cnf(Neg(And([Var("p"), Var("q")])))), "(~p | ~q)")
        self.assertEqual(str(cnf(Neg(And([Var("p"), Var("q"), Var("p")])))), "(~q | ~p)")
        self.assertEqual(str(cnf(Neg(And([And([Var("p"), Var("q")]), Var("p")])))), "(~q | ~p)")
        self.assertEqual(str(cnf(Neg(And([Const(True), Const(False)])))), "True")
        self.assertEqual(str(cnf(Neg(And([Const(False), Const(False)])))), "True")
        self.assertEqual(str(cnf(Neg(And([Const(True), Const(True)])))), "False")
        self.assertEqual(str(cnf(Neg(And([Const(True), Var("p")])))), "~p")

        self.assertEqual(str(cnf(And([Or([Var("p"), Var("q")]), Or([Var("p"), Var("r")])]))), "((p | q) & (p | r))")
        self.assertEqual(str(cnf(Or([And([Var("p"), Var("q")]), Const(False)]))), "(p & q)")
        self.assertEqual(str(cnf(Or([And([Var("p"), Var("q")]), And([Var("r"), Var("q")])]))), "((p | r) & (p | q) & (q | r) & q)")
        self.assertEqual(str(cnf(Neg(Or([And([Var("p"), Var("q")]), And([Var("r"), Var("q")])])))), "((~p | ~q) & (~r | ~q))")
        self.assertEqual(str(cnf(Or([And([Var("p"), Var("q")]), Or([Var("r"), Var("q")])]))) , "((p | r | q) & (r | q))")
        self.assertEqual(str(cnf(Or([Or([And([Var("p"), Var("q")]), Var("r")]), And([Var("r"), Var("s")])]))), "((p | r) & (p | r | s) & (q | r) & (q | r | s))")
        self.assertEqual(str(cnf(Or([And([Var("p"), Or([Var("q"), Var("r")])]), And([Var("r"), Var("s")])]))), "((p | r) & (p | s) & (q | r) & (q | r | s))")
        self.assertEqual(str(cnf(Or([Or([And([Var("p"), Var("q")]), Var("r")]), Neg(Var("q"))]))), "(p | r | ~q)")


    def test_simplify(self):
        self.assertEqual(str(simplify(Var("p"))), "p")
        self.assertEqual(str(simplify(Const(True))), "True")
        self.assertEqual(str(simplify(Or([Var("p"), Var("q")]))), "(p | q)")
        self.assertEqual(str(simplify(Or([Var("p"), Var("q"), Var("p")]))), "(q | p)")
        self.assertEqual(str(simplify(Or([Or([Var("p"), Var("q")]), Var("p")]))), "(q | p)")
        self.assertEqual(str(simplify(Or([Const(True), Const(False)]))), "True")
        self.assertEqual(str(simplify(Or([Const(False), Const(False)]))), "False")
        self.assertEqual(str(simplify(Or([Const(True), Const(True)]))), "True")
        self.assertEqual(str(simplify(Or([Const(True), Var("p")]))), "True")
        self.assertEqual(str(simplify(And([Var("p"), Var("q")]))), "(p & q)")
        self.assertEqual(str(simplify(And([Var("p"), Var("q"), Var("p")]))), "(q & p)")
        self.assertEqual(str(simplify(And([And([Var("p"), Var("q")]), Var("p")]))), "(q & p)")
        self.assertEqual(str(simplify(And([Const(True), Const(False)]))), "False")
        self.assertEqual(str(simplify(And([Const(False), Const(False)]))), "False")
        self.assertEqual(str(simplify(And([Const(True), Const(True)]))), "True")
        self.assertEqual(str(simplify(And([Const(True), Var("p")]))), "p")

        self.assertEqual(str(simplify(Neg(Var("p")))), "~p")
        self.assertEqual(str(simplify(Neg(Neg(Var("p"))))), "p")
        self.assertEqual(str(simplify(Neg(Const(True)))), "False")
        self.assertEqual(str(simplify(Neg(Or([Var("p"), Var("q")])))), "(~p & ~q)")
        self.assertEqual(str(simplify(Neg(Or([Var("p"), Var("q"), Var("p")])))), "(~q & ~p)")
        self.assertEqual(str(simplify(Neg(Or([Or([Var("p"), Var("q")]), Var("p")])))), "(~q & ~p)")
        self.assertEqual(str(simplify(Neg(Or([Const(True), Const(False)])))), "False")
        self.assertEqual(str(simplify(Neg(Or([Const(False), Const(False)])))), "True")
        self.assertEqual(str(simplify(Neg(Or([Const(True), Const(True)])))), "False")
        self.assertEqual(str(simplify(Neg(Or([Const(True), Var("p")])))), "False")
        self.assertEqual(str(simplify(Neg(And([Var("p"), Var("q")])))), "(~p | ~q)")
        self.assertEqual(str(simplify(Neg(And([Var("p"), Var("q"), Var("p")])))), "(~q | ~p)")
        self.assertEqual(str(simplify(Neg(And([And([Var("p"), Var("q")]), Var("p")])))), "(~q | ~p)")
        self.assertEqual(str(simplify(Neg(And([Const(True), Const(False)])))), "True")
        self.assertEqual(str(simplify(Neg(And([Const(False), Const(False)])))), "True")
        self.assertEqual(str(simplify(Neg(And([Const(True), Const(True)])))), "False")
        self.assertEqual(str(simplify(Neg(And([Const(True), Var("p")])))), "~p")
        self.assertEqual(str(simplify(Neg(And([Neg(Or([Neg(Var("p")), Var("q")])), Neg(And([Var("q"), Const(False)]))])))), "(~p | q)")


    def test_simplify_cnf(self):
        self.assertEqual(str(simplify_cnf(Var("p"), {"p": True})), "True")
        self.assertEqual(str(simplify_cnf(Const(True), {})), "True")
        self.assertEqual(str(simplify_cnf(Or([Var("p"), Var("q")]), {"p": True, "q": False})), "True")
        self.assertEqual(str(simplify_cnf(Or([Var("p"), Var("q"), Var("p")]), {"p": True, "q": False})), "True")
        self.assertEqual(str(simplify_cnf(Or([Or([Var("p"), Var("q")]), Var("p")]), {"p": True, "q": False})), "True")
        self.assertEqual(str(simplify_cnf(Or([Const(True), Const(False)]), {})), "True")
        self.assertEqual(str(simplify_cnf(Or([Const(False), Const(False)]), {})), "False")
        self.assertEqual(str(simplify_cnf(Or([Const(True), Const(True)]), {})), "True")
        self.assertEqual(str(simplify_cnf(Or([Const(True), Var("p")]), {"p": True})), "True")
        self.assertEqual(str(simplify_cnf(And([Var("p"), Var("q")]), {"p": False, "q": True})), "False")
        self.assertEqual(str(simplify_cnf(And([Var("p"), Var("q"), Var("p")]), {"p": False, "q": True})), "False")
        self.assertEqual(str(simplify_cnf(And([And([Var("p"), Var("q")]), Var("p")]), {"p": False, "q": True})), "False")
        self.assertEqual(str(simplify_cnf(And([Const(True), Const(False)]), {})), "False")
        self.assertEqual(str(simplify_cnf(And([Const(False), Const(False)]), {})), "False")
        self.assertEqual(str(simplify_cnf(And([Const(True), Const(True)]), {})), "True")
        self.assertEqual(str(simplify_cnf(And([Const(True), Var("p")]), {"p": False})), "False")

        self.assertEqual(str(simplify_cnf(Neg(Var("p")), {"p": False})), "True")
        self.assertEqual(str(simplify_cnf(Neg(Neg(Var("p"))), {"p": True})), "True")
        self.assertEqual(str(simplify_cnf(Neg(Const(True)), {})), "False")
        self.assertEqual(str(simplify_cnf(Neg(Or([Var("p"), Var("q")])), {"p": False, "q": True})), "False")
        self.assertEqual(str(simplify_cnf(Neg(Or([Var("p"), Var("q"), Var("p")])), {"p": False, "q": True})), "False")
        self.assertEqual(str(simplify_cnf(Neg(Or([Or([Var("p"), Var("q")]), Var("p")])), {"p": False, "q": True})), "False")
        self.assertEqual(str(simplify_cnf(Neg(Or([Const(True), Const(False)])), {})), "False")
        self.assertEqual(str(simplify_cnf(Neg(Or([Const(False), Const(False)])), {})), "True")
        self.assertEqual(str(simplify_cnf(Neg(Or([Const(True), Const(True)])), {})), "False")
        self.assertEqual(str(simplify_cnf(Neg(Or([Const(True), Var("p")])), {"p": False})), "False")
        self.assertEqual(str(simplify_cnf(Neg(And([Var("p"), Var("q")])), {"p": False, "q": True})), "True")
        self.assertEqual(str(simplify_cnf(Neg(And([Var("p"), Var("q"), Var("p")])), {"p": False, "q": True})), "True")
        self.assertEqual(str(simplify_cnf(Neg(And([And([Var("p"), Var("q")]), Var("p")])), {"p": False, "q": True})), "True")
        self.assertEqual(str(simplify_cnf(Neg(And([Const(True), Const(False)])), {})), "True")
        self.assertEqual(str(simplify_cnf(Neg(And([Const(False), Const(False)])), {})), "True")
        self.assertEqual(str(simplify_cnf(Neg(And([Const(True), Const(True)])), {})), "False")
        self.assertEqual(str(simplify_cnf(Neg(And([Const(True), Var("p")])), {"p": True})), "False")

        self.assertEqual(str(simplify_cnf(And([Or([Var("p"), Var("q")]), Or([Var("p"), Var("r")])]), {"p": True, "q": False, "r": False})), "True")
        self.assertEqual(str(simplify_cnf(Or([And([Var("p"), Var("q")]), Const(False)]), {"p": True, "q": False})), "False")
        self.assertEqual(str(simplify_cnf(Or([And([Var("p"), Var("q")]), And([Var("r"), Var("q")])]), {"p": True, "q": False, "r": True})), "False")
        self.assertEqual(str(simplify_cnf(Neg(And([And([Var("p"), Var("q")]), And([Var("r"), Var("q")])])), {"p": True, "q": False, "r": False})), "True")
        self.assertEqual(str(simplify_cnf(Or([And([Var("p"), Var("q")]), Or([Var("r"), Var("q")])]), {"p": False, "q": False, "r": True})), "True")
        self.assertEqual(str(simplify_cnf(Or([Or([And([Var("p"), Var("q")]), Var("r")]), And([Var("r"), Var("s")])]), {"p": True, "q": False, "r": False, "s": False})), "False")
        self.assertEqual(str(simplify_cnf(Or([And([Var("p"), Or([Var("q"), Var("r")])]), And([Var("r"), Var("s")])]), {"p": True, "q": False, "r": False, "s": True})), "False")
        self.assertEqual(str(simplify_cnf(Or([Or([And([Var("p"), Var("q")]), Var("r")]), Neg(Var("q"))]), {"p": False, "q": True, "r": False})), "False")


    def test_solve(self):
        self.assertEqual(str(solve(Var("p"), {"p": True})), "True")
        self.assertEqual(str(solve(Const(True), {})), "True")
        self.assertEqual(str(solve(Or([Var("p"), Var("q")]), {"p": True, "q": False})), "True")
        self.assertEqual(str(solve(Or([Var("p"), Var("q"), Var("p")]), {"p": True, "q": False})), "True")
        self.assertEqual(str(solve(Or([Or([Var("p"), Var("q")]), Var("p")]), {"p": True, "q": False})), "True")
        self.assertEqual(str(solve(Or([Const(True), Const(False)]), {})), "True")
        self.assertEqual(str(solve(Or([Const(False), Const(False)]), {})), "False")
        self.assertEqual(str(solve(Or([Const(True), Const(True)]), {})), "True")
        self.assertEqual(str(solve(Or([Const(True), Var("p")]), {"p": True})), "True")
        self.assertEqual(str(solve(And([Var("p"), Var("q")]), {"p": False, "q": True})), "False")
        self.assertEqual(str(solve(And([Var("p"), Var("q"), Var("p")]), {"p": False, "q": True})), "False")
        self.assertEqual(str(solve(And([And([Var("p"), Var("q")]), Var("p")]), {"p": False, "q": True})), "False")
        self.assertEqual(str(solve(And([Const(True), Const(False)]), {})), "False")
        self.assertEqual(str(solve(And([Const(False), Const(False)]), {})), "False")
        self.assertEqual(str(solve(And([Const(True), Const(True)]), {})), "True")
        self.assertEqual(str(solve(And([Const(True), Var("p")]), {"p": False})), "False")

        self.assertEqual(str(solve(Neg(Var("p")), {"p": False})), "True")
        self.assertEqual(str(solve(Neg(Neg(Var("p"))), {"p": True})), "True")
        self.assertEqual(str(solve(Neg(Const(True)), {})), "False")
        self.assertEqual(str(solve(Neg(Or([Var("p"), Var("q")])), {"p": False, "q": True})), "False")
        self.assertEqual(str(solve(Neg(Or([Var("p"), Var("q"), Var("p")])), {"p": False, "q": True})), "False")
        self.assertEqual(str(solve(Neg(Or([Or([Var("p"), Var("q")]), Var("p")])), {"p": False, "q": True})), "False")
        self.assertEqual(str(solve(Neg(Or([Const(True), Const(False)])), {})), "False")
        self.assertEqual(str(solve(Neg(Or([Const(False), Const(False)])), {})), "True")
        self.assertEqual(str(solve(Neg(Or([Const(True), Const(True)])), {})), "False")
        self.assertEqual(str(solve(Neg(Or([Const(True), Var("p")])), {"p": False})), "False")
        self.assertEqual(str(solve(Neg(And([Var("p"), Var("q")])), {"p": False, "q": True})), "True")
        self.assertEqual(str(solve(Neg(And([Var("p"), Var("q"), Var("p")])), {"p": False, "q": True})), "True")
        self.assertEqual(str(solve(Neg(And([And([Var("p"), Var("q")]), Var("p")])), {"p": False, "q": True})), "True")
        self.assertEqual(str(solve(Neg(And([Const(True), Const(False)])), {})), "True")
        self.assertEqual(str(solve(Neg(And([Const(False), Const(False)])), {})), "True")
        self.assertEqual(str(solve(Neg(And([Const(True), Const(True)])), {})), "False")
        self.assertEqual(str(solve(Neg(And([Const(True), Var("p")])), {"p": True})), "False")

        self.assertEqual(str(solve(Or([Const(False), Const(True)]), {})), "True")
        self.assertEqual(str(solve(And([Const(False), Neg(Const(False))]), {})), "False")
        self.assertEqual(str(solve(Neg(Var("p")), {"p": True})) , "False")
        self.assertEqual(str(solve(Neg(And([Var("p"), Var("q"), Var("p")])), {"p": True, "q": False})), "True")
        self.assertEqual(str(solve(Neg(Or([Var("p"), Var("q"), Var("p")])), {"p": True, "q": False})), "False")
        self.assertEqual(str(solve(And([Or([Neg(Var("p")), Var("q")]), Neg(And([Var("q"), Const(False)])), Or([Var("r"), Var("p")])]), {"p": False, "q": True, "r": True})), "True")


    def test_sat(self):
        self.assertEqual(sat(Var("p"), {}), (True, {'p': True}))
        self.assertEqual(sat(Const(True), {}), (True, {}))
        self.assertEqual(sat(Or([Var("p"), Var("q")]), {}), (True, {'q': True, 'p': True}))
        self.assertEqual(sat(Or([Var("p"), Var("q"), Var("p")]), {}), (True, {'q': True, 'p': True}))
        self.assertEqual(sat(Or([Or([Var("p"), Var("q")]), Var("p")]), {}), (True, {'q': True, 'p': True}))
        self.assertEqual(sat(Or([Const(True), Const(False)]), {}), (True, {}))
        self.assertEqual(sat(Or([Const(False), Const(False)]), {}), (False, {}))
        self.assertEqual(sat(Or([Const(True), Const(True)]), {}), (True, {}))
        self.assertEqual(sat(Or([Const(True), Var("p")]), {}), (True, {}))
        self.assertEqual(sat(And([Var("p"), Var("q")]), {}), (True, {'q': True, 'p': True}))
        self.assertEqual(sat(And([Var("p"), Var("q"), Var("p")]), {}), (True, {'q': True, 'p': True}))
        self.assertEqual(sat(And([And([Var("p"), Var("q")]), Var("p")]), {}), (True, {'q': True, 'p': True}))
        self.assertEqual(sat(And([Const(True), Const(False)]), {}), (False, {}))
        self.assertEqual(sat(And([Const(False), Const(False)]), {}), (False, {}))
        self.assertEqual(sat(And([Const(True), Const(True)]), {}), (True, {}))
        self.assertEqual(sat(And([Const(True), Var("p")]), {}), (True, {'p': True}))

        self.assertEqual(sat(Neg(Var("p")), {}), (True, {'p': False}))
        self.assertEqual(sat(Neg(Neg(Var("p"))), {}), (True, {'p': True}))
        self.assertEqual(sat(Neg(Const(True)), {}), (False, {}))
        self.assertEqual(sat(Neg(Or([Var("p"), Var("q")])), {}), (True, {'q': False, 'p': False}))
        self.assertEqual(sat(Neg(Or([Var("p"), Var("q"), Var("p")])), {}), (True, {'q': False, 'p': False}))
        self.assertEqual(sat(Neg(Or([Or([Var("p"), Var("q")]), Var("p")])), {}), (True, {'q': False, 'p': False}))
        self.assertEqual(sat(Neg(Or([Const(True), Const(False)])), {}), (False, {}))
        self.assertEqual(sat(Neg(Or([Const(False), Const(False)])), {}), (True, {}))
        self.assertEqual(sat(Neg(Or([Const(True), Const(True)])), {}), (False, {}))
        self.assertEqual(sat(Neg(Or([Const(True), Var("p")])), {}), (False, {}))
        self.assertEqual(sat(Neg(And([Var("p"), Var("q")])), {}), (True, {'q': False, 'p': False}))
        self.assertEqual(sat(Neg(And([Var("p"), Var("q"), Var("p")])), {}), (True, {'q': False, 'p': False}))
        self.assertEqual(sat(Neg(And([And([Var("p"), Var("q")]), Var("p")])), {}), (True, {'q': False, 'p': False}))
        self.assertEqual(sat(Neg(And([Const(True), Const(False)])), {}), (True, {}))
        self.assertEqual(sat(Neg(And([Const(False), Const(False)])), {}), (True, {}))
        self.assertEqual(sat(Neg(And([Const(True), Const(True)])), {}), (False, {}))
        self.assertEqual(sat(Neg(And([Const(True), Var("p")])), {}), (True, {'p': False}))

        self.assertEqual(sat(And([Var("p"), Neg(Var("p"))]), {}), (False, {}))
        self.assertEqual(sat(And([Var("p"), Var("p")]), {}), (True, {'p': True}))
        self.assertEqual(sat(And([Var("p"), Const(False)]), {}), (False, {}))
        self.assertEqual(sat(And([Var("p"), Const(True)]), {}), (True, {'p': True}))
        self.assertEqual(sat(Or([Var("p"), Var("q"), Const(True)]), {}),  (True, {}))
        self.assertEqual(sat(Or([Neg(And([Var("p"), Var("q")])), And([Var("p"), Var("r")])]), {}), (True, {'q': False, 'p': False, 'r': True}))
        self.assertEqual(sat(And([And([Var("p"), Var("q")]), And([Var("p"), Neg(Var("q"))]), Var("s")]), {}), (False, {}))
        self.assertEqual(sat(And([Or([Var("p"), Var("q")]), And([Var("p"), Neg(Var("q"))]), Var("s")]), {}), (True, {'q': False, 'p': True, 's': True}))
        self.assertEqual(sat(And([Or([Var("p"), Var("q")]), And([Var("p"), Neg(Var("q"))]), Var("s")]), {"p": False}), (False, {}))


    def test_sudoku(self):
        # Two equal numbers in the same row
        sudoku = [[2, 1, 1, 3, "", "", 4, "", ""],
                  ["", "", "", 4, 6, "", "", "", 5],
                  ["", "", "", "", "", 5, 7, "", ""],
                  ["", 9, "", "", "", "", "", 2, ""],
                  [8, "", "", "", "", "", "", "", ""],
                  ["", 3, "", "", 8, "", "", 9, 1],
                  [6, 2, "", "", "", 9, "", "", ""],
                  ["", "", 9, 6, "", "", 8, "", ""],
                  ["", "", "", 7, 3, "", "", 5, ""]]
        self.assertEqual(sat(sudoku2SAT(sudoku), {}), (False, {}))

        # Two equal numbers in the same column
        sudoku = [[2, 1, "", 3, "", "", 4, "", ""],
                  ["", "", "", 4, 6, "", "", "", 5],
                  ["", "", "", "", "", 5, 7, "", ""],
                  [8, 9, "", "", "", "", "", 2, ""],
                  [8, "", "", "", "", "", "", "", ""],
                  ["", 3, "", "", 8, "", "", 9, 1],
                  [6, 2, "", "", "", 9, "", "", ""],
                  ["", "", 9, 6, "", "", 8, "", ""],
                  ["", "", "", 7, 3, "", "", 5, ""]]
        self.assertEqual(sat(sudoku2SAT(sudoku), {}), (False, {}))

        # Two equal numbers in the same 3x3 square
        sudoku = [[2, 1, "", 3, "", "", 4, "", ""],
                    ["", "", 1, 4, 6, "", "", "", 5],
                    ["", "", "", "", "", 5, 7, "", ""],
                    ["", 9, "", "", "", "", "", 2, ""],
                    [8, "", "", "", "", "", "", "", ""],
                    ["", 3, "", "", 8, "", "", 9, 1],
                    [6, 2, "", "", "", 9, "", "", ""],
                    ["", "", 9, 6, "", "", 8, "", ""],
                    ["", "", "", 7, 3, "", "", 5, ""]]
        self.assertEqual(sat(sudoku2SAT(sudoku), {}), (False, {}))


    def test_graph2SAT(self):
        # Cyclic graph on odd number of points
        V = ["v1", "v2", "v3"]
        E = {"v1v2": 1, "v2v3": 1, "v3v1": 1}
        self.assertEqual(sat(graph2SAT(V,E,2), {}), (False, {}))
        self.assertEqual(sat(graph2SAT(V,E,3), {}), (True, {'C2,3': False, 'C2,2': True, 'C2,1': False, 'C3,2': False, 'C3,3': True, 'C3,1': False, 'C1,1': True, 'C1,2': False, 'C1,3': False}))

        # Cyclic graph on even number of points
        V = ["v1", "v2", "v3", "v4"]
        E = {"v1v2": 1, "v2v3": 1, "v3v4": 1, "v4v1": 1}
        self.assertEqual(sat(graph2SAT(V,E,2), {}), (True, {'C2,2': True, 'C2,1': False, 'C4,1': False, 'C4,2': True, 'C3,2': False, 'C3,1': True, 'C1,1': True, 'C1,2': False}))

        # Bipartite graph
        V = ["v1", "v2", "v3", "v4"]
        E = {"v1v3": 1, "v1v4": 1, "v2v4": 1}
        self.assertEqual(sat(graph2SAT(V,E,2), {}), (True, {'C2,2': False, 'C2,1': True, 'C4,1': False, 'C4,2': True, 'C3,2': True, 'C3,1': False, 'C1,1': True, 'C1,2': False}))

        # Complete graph
        V = ["v1", "v2", "v3", "v4"]
        E = {"v1v2": 1, "v1v3": 1, "v1v4": 1, "v2v3": 1, "v2v4": 1, "v3v4": 1}
        self.assertEqual(sat(graph2SAT(V,E,2), {}), (False, {}))
        self.assertEqual(sat(graph2SAT(V,E,3), {}), (False, {}))
        self.assertEqual(sat(graph2SAT(V,E,4), {}), (True, {'C2,3': False, 'C2,2': True, 'C2,1': False, 'C4,1': False, 'C4,3': False, 'C4,2': False, 'C2,4': False, 'C3,2': False, 'C3,3': True, 'C3,1': False, 'C3,4': False, 'C1,1': True, 'C1,2': False, 'C1,3': False, 'C1,4': False, 'C4,4': True}))

        # Tree
        V = ["v1", "v2", "v3", "v4", "v5"]
        E = {"v1v2": 1, "v1v3": 1, "v3v4": 1, "v3v5": 1}
        self.assertEqual(sat(graph2SAT(V,E,2), {}), (True, {'C2,2': True, 'C2,1': False, 'C4,1': True, 'C4,2': False, 'C3,2': True, 'C3,1': False, 'C1,1': True, 'C1,2': False, 'C5,1': True, 'C5,2': False}))

        # Petersen graph
        V = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10"]
        E = {"v1v2": 1, "v1v5": 1, "v1v6": 1, "v2v3": 1, "v2v7": 1, "v3v4": 1, "v3v8": 1, "v4v5": 1, "v4v9": 1, "v5v10": 1, "v6v8": 1, "v6v9": 1, "v7v9": 1, "v7v10": 1, "v8v10": 1}
        self.assertEqual(sat(graph2SAT(V,E,2), {}), (False, {}))
        self.assertEqual(sat(graph2SAT(V,E,3), {}), (True, {'C9,1': False, 'C9,2': False, 'C9,3': True, 'C6,3': False, 'C6,2': True, 'C6,1': False, 'C8,1': False, 'C8,3': True, 'C8,2': False, 'C10,1': False, 'C10,3': False, 'C10,2': True, 'C3,2': False, 'C3,3': False, 'C3,1': True, 'C1,1': True, 'C1,2': False, 'C1,3': False, 'C2,3': False, 'C2,2': True, 'C2,1': False, 'C4,1': False, 'C4,3': False, 'C4,2': True, 'C7,2': False, 'C7,3': False, 'C7,1': True, 'C5,1': False, 'C5,2': False, 'C5,3': True}))


if __name__ == '__main__':
    unittest.main()
