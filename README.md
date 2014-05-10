LVR SAT solver
=======

**Authors:** _Martin Jakomin_ & _Mateja Rojko_

SAT solver created as a project work at course LVR (Logic in Computer Science).
It contains the structures for boolean operators and expressions, various functions for expression manipulation
and simplification, SAT solver based on DPLL algorithm and some methods for conversion of some known problems
to bool expressions, such as graph coloring and sudoku.

___


## Algorithm
The implementation of our sat solver is based on DPLL algorithm (http://en.wikipedia.org/wiki/DPLL_algorithm),
with various improvements, such as loop simplification and sorting the clauses by their length.

[Povejte, kateri algoritem ste uporabili, dodajte link na opis algoritma. Če ste algoritem priredili ali nadgradili,
ali če je v zvezi z vašo implementacijo kaj omembe vrednega, to tudi napišite.]


## Project structure
 * `SAT/` contains the source code:
   * `SAT/bool.py` contains the classes for boolean constructs (operators) and expressions, and functions: nnf, simplify, cnf, solve, simplify_cnf
   * `SAT/sat.py` contains the sat solver (modified DPLL algorithm)
   * `SAT/sat_converter.py` contains the methods for converting the graph coloring problem and Sudoku to Boolean expressions
   * `SAT/test.py` contains te unit tests for the project


## Instructions
[Napišite tudi kratka navodila, kako se vaša koda uporabi. Najbolje je, da priložite primere.
V zvezi s tem glejte nalogi 6 in 7.]









