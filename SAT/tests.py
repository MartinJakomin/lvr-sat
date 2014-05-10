_author__ = 'Martin Jakomin, Mateja Rojko'

from sat import sat
from bool import Var, Neg, And, Or, Const, cnf, simplify_cnf, nnf, simplify, solve
import unittest


class MyTest(unittest.TestCase):
    def testSat(self):
        self.assertEqual(sat(And([Var("p"), Neg(Var("p"))]), {}), (False, {}))
        self.assertEqual(sat(And([Var("p"), Var("p")]), {}), (True, {'p': True}))
        self.assertEqual(sat(And([Var("p"), Const(False)]), {}), (False, {}))
        self.assertEqual(sat(And([Var("p"), Const(True)]), {}), (True, {'p': True}))
        self.assertEqual(sat(Or([Var("p"), Var("q"), Const(True)]), {}),  (True, {}))
        self.assertEqual(sat(Or([Neg(And([Var("p"), Var("q")])), And([Var("p"), Var("r")])]), {}), (True, {'q': False, 'p': False, 'r': True}))
        self.assertEqual(sat(And([And([Var("p"), Var("q")]), And([Var("p"), Neg(Var("q"))]), Var("s")]), {}), (False, {}))
        self.assertEqual(sat(And([Or([Var("p"), Var("q")]), And([Var("p"), Neg(Var("q"))]), Var("s")]), {}), (True, {'q': False, 'p': True, 's': True}))
        self.assertEqual(sat(And([Or([Var("p"), Var("q")]), And([Var("p"), Neg(Var("q"))]), Var("s")]), {"p": False}), (False, {}))


    def testNnf(self):
        self.assertEqual(str(nnf(Var("p"))), "p")
        self.assertEqual(str(nnf(Const(True))) , "True")
        self.assertEqual(str(nnf(Or([Var("p"), Var("q")]))), "(p | q)")
        self.assertEqual(str(nnf(And([Var("p"), Var("q")]))), "(p & q)")
        self.assertEqual(str(nnf(Or([Var("p"), Var("q"), Var("p")]))), "(p | q | p)")
        self.assertEqual(str(nnf(Neg(Var("p")))), "~p")
        self.assertEqual(str(nnf(Neg(Const(True)))), "False")
        self.assertEqual(str(nnf(Neg(Neg(Var("p"))))), "p")
        self.assertEqual(str(nnf(Neg(Or([Var("p"), Var("q")])))), "(~p & ~q)")
        self.assertEqual(str(nnf(Neg(And([Var("p"), Var("q")])))), "(~p | ~q)")
        self.assertEqual(str(nnf(Neg(Or([Var("p"), Var("q"), Var("p")])))), "(~p & ~q & ~p)")
        self.assertEqual(str(nnf(And([Neg(Const(True)), Const(False)]))), "(False & False)")
        self.assertEqual(str(nnf(Or([Neg(Const(True)), Const(True)]))), "(False | True)")
        self.assertEqual(str(nnf(Neg(And([Neg(Or([Neg(Var("p")), Var("q")])), Neg(And([Var("q"), Const(False)]))])))), "((~p | q) | (q & False))")


    def testSimplify(self):
        self.assertEqual(str(simplify(Neg(Neg(Var("p"))))), "p")
        self.assertEqual(str(simplify(Neg(Or([Var("p"), Var("q")])))), "(~p & ~q)")
        self.assertEqual(str(simplify(Neg(And([Var("p"), Var("q")])))), "(~p | ~q)")
        self.assertEqual(str(simplify(Neg(Or([Var("p"), Var("q"), Var("p")])))), "(~q & ~p)")
        self.assertEqual(str(simplify(Neg(Const(True)))), "False")
        self.assertEqual(str(simplify(And([Neg(Const(True)), Const(False)]))), "False")
        self.assertEqual(str(simplify(Or([Neg(Const(True)), Const(True)]))), "True")
        self.assertEqual(str(simplify(Neg(And([Neg(Or([Neg(Var("p")), Var("q")])), Neg(And([Var("q"), Const(False)]))])))), "(~p | q)")


    def testSolve(self):
        self.assertEqual(str(solve(Or([Const(False), Const(True)]), {})), "True")
        self.assertEqual(str(solve(And([Const(False), Neg(Const(False))]), {})), "False")
        self.assertEqual(str(solve(Neg(Var("p")), {"p": True})) , "False")
        self.assertEqual(str(solve(Neg(And([Var("p"), Var("q"), Var("p")])), {"p": True, "q": False})), "True")
        self.assertEqual(str(solve(Neg(Or([Var("p"), Var("q"), Var("p")])), {"p": True, "q": False})), "False")
        self.assertEqual(str(solve(And([Or([Neg(Var("p")), Var("q")]), Neg(And([Var("q"), Const(False)])), Or([Var("r"), Var("p")])]), {"p": False, "q": True, "r": True})), "True")


    def testCnf(self):
        self.assertEqual(str(cnf(And([Or([Var("p"), Var("q")]), Or([Var("p"), Var("r")])]))), "((p | q) & (p | r))")
        self.assertEqual(str(cnf(Or([And([Var("p"), Var("q")]), Const(False)]))), "(p & q)")
        self.assertEqual(str(cnf(Or([And([Var("p"), Var("q")]), And([Var("r"), Var("q")])]))), "((p | r) & (p | q) & (q | r) & q)")
        self.assertEqual(str(cnf(Neg(Or([And([Var("p"), Var("q")]), And([Var("r"), Var("q")])])))), "((~p | ~q) & (~r | ~q))")
        self.assertEqual(str(cnf(Or([And([Var("p"), Var("q")]), Or([Var("r"), Var("q")])]))) , "((p | r | q) & (r | q))")
        self.assertEqual(str(cnf(Or([Or([And([Var("p"), Var("q")]), Var("r")]), And([Var("r"), Var("s")])]))), "((p | r) & (p | r | s) & (q | r) & (q | r | s))")
        self.assertEqual(str(cnf(Or([And([Var("p"), Or([Var("q"), Var("r")])]), And([Var("r"), Var("s")])]))), "((p | r) & (p | s) & (q | r) & (q | r | s))")
        self.assertEqual(str(cnf(Or([Or([And([Var("p"), Var("q")]), Var("r")]), Neg(Var("q"))]))), "(p | r | ~q)")


    def testSimplify_cnf(self):
        self.assertEqual(str(simplify_cnf(And([Or([Var("p"), Var("q")]), Or([Var("p"), Var("r")])]), {"p": True, "q": False, "r": False})), "True")
        self.assertEqual(str(simplify_cnf(Or([And([Var("p"), Var("q")]), Const(False)]), {"p": True, "q": False})), "False")
        self.assertEqual(str(simplify_cnf(Or([And([Var("p"), Var("q")]), And([Var("r"), Var("q")])]), {"p": True, "q": False, "r": True})), "False")
        #self.assertEqual(str(simplify_cnf(Neg(And([And([Var("p"), Var("q")]), And([Var("r"), Var("q")])])), {"p": True, "q": False, "r": False})), "True")
        #!!!  self.assertEqual(str(simplify_cnf(Neg(Or([Var("p"), Var("q")])), {"p": True, "q": True})), "False")
        self.assertEqual(str(simplify_cnf(Or([And([Var("p"), Var("q")]), Or([Var("r"), Var("q")])]), {"p": False, "q": False, "r": True})), "True")
        self.assertEqual(str(simplify_cnf(Or([Or([And([Var("p"), Var("q")]), Var("r")]), And([Var("r"), Var("s")])]), {"p": True, "q": False, "r": False, "s": False})), "False")
        self.assertEqual(str(simplify_cnf(Or([And([Var("p"), Or([Var("q"), Var("r")])]), And([Var("r"), Var("s")])]), {"p": True, "q": False, "r": False, "s": True})), "False")
        self.assertEqual(str(simplify_cnf(Or([Or([And([Var("p"), Var("q")]), Var("r")]), Neg(Var("q"))]), {"p": False, "q": True, "r": False})), "False")


if __name__ == '__main__':
    unittest.main()
