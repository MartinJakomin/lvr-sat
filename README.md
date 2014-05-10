LVR SAT solver
=======

**Authors:** _Martin Jakomin_ & _Mateja Rojko_

SAT solver created as a project work at course LVR (Logic in Computer Science).
It contains the structures for boolean operators and expressions, various functions for expression manipulation
and simplification, SAT solver based on DPLL algorithm and methods for conversion of some known problems
to Boolean expressions, such as graph coloring and sudoku.

___


## Algorithm
The implementation of our sat solver is based on DPLL algorithm (http://en.wikipedia.org/wiki/DPLL_algorithm),
with various improvements, such as loop simplification and sorting the clauses by their length.


## Project structure
 * `SAT/` contains the source code:
   * `SAT/bool.py` contains the classes for boolean constructs (operators) and expressions, and functions for expression
   manipulation and simplification
   * `SAT/sat.py` contains the sat solver (modified DPLL algorithm)
   * `SAT/sat_converter.py` contains the methods for converting the graph coloring problem and Sudoku to Boolean expressions
   * `SAT/test.py` contains te unit tests for the project


## Instructions
 * Building the expression: By using constructs such as Var, Neg, Or, And and Const you can build any Boolean expression.
 Variables are defined with: Var("Variable name"), Negation with Neg(_expression_), constant with Const(_True_/_False_),
 And clause with And([_List of literals or expressions_]) and similar Or clause with Or([_List of literals or expressions_]).

 * Expression manipulation and simplification: In `bool.py` you can find various functions, such as nnf, simplify, cnf, solve and simplify_cnf.
 For conversion to Negation normal form you can use **nnf**(_expression_), similar you can use **cnf**(_expression_) for conversion
  to Conjunctive normal form. You can simplify the expression with **simplify**(_expression_) or **simplify_cnf**(_expression_,_dictionary of set literals_)
  which will simplify the expression using the set variables and convert it to CNF form (some kind of partial solve). For
  complete solving of an expression you must provide full variable setting in a dictionary of form {"variable name": _True_/_False_}
  and then call the function **solve**(_expression_,_variable setting_).

 * SAT

 * Conversion of known problems