__author__ = "Martin Jakomin, Mateja Rojko"


"""
Classes for boolean operators:
- Var
- Neg
- Or
- And
- Const

Functions:
- nnf
- simplify
- cnf
- solve
- simplify_cnf
"""

import itertools


# functions


def nnf(f):
    """ Returns negation normal form """
    return f.nnf()


def simplify(f):
    """ Simplifies the expression """
    return nnf(f).simplify()


def cnf(f):
    """ Returns conjunctive normal form """
    return nnf(f).cnf().simplify()


def solve(f, v):
    """ Solves the expression using the variable values v """
    return f.solve(v)


def simplify_cnf(f, v):
    """ Simplifies the cnf form using the variable values v """
    return cnf(f.simplify_cnf(v))


# classes


class Var():
    """
    Variable
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def solve(self, v):
        return v[self.name]

    def simplify_cnf(self, v):
        if self.name in v:
            return Const(v[self.name])
        else:
            return self

    def nnf(self):
        return self

    def simplify(self):
        return self

    def cnf(self):
        return self

    def length(self):
        return 1


class Neg():
    """
    Negation operator
    """

    def __init__(self,v):
        self.value = v

    def __str__(self):
        return "~" + str(self.value.__str__())

    def solve(self, v):
        return not(self.value.solve(v))

    def simplify_cnf(self, v):
        if self.value.name in v:
            return Const(not(v[self.value.name]))
        else:
            return self

    def nnf(self):
        v = self.value
        if isinstance(v, Var):
            return Neg(v)
        elif isinstance(v, Neg):
            return v.value.nnf()
        elif isinstance(v, And):
            return Or([Neg(x) for x in v.value]).nnf()
        elif isinstance(v, Or):
            return And([Neg(x) for x in v.value]).nnf()
        elif isinstance(v, Const):
            return v.negate()

    def simplify(self):
        return self

    def cnf(self):
        return self

    def length(self):
        return self.value.length()


class And():
    """
    And operator
    """

    def __init__(self,lst):
        self.value = lst

    def __str__(self):
        s = "("
        for i in self.value:
            s += str(i)+" & "
        s = s[:len(s)-3]
        return s + ")"

    def solve(self, v):
        for l in self.value:
            if l.solve(v) is False:
                return False
        return True

    def simplify_cnf(self, v):
        return And([x.simplify_cnf(v) for x in self.value])

    def nnf(self):
        return And([x.nnf() for x in self.value])

    def simplify(self):
        s = [x.simplify() for x in self.value]
        # And list flatten
        ns = []
        for x in s:
            if isinstance(x, And):
                ns.extend(x.value)
            else:
                ns.append(x)
        s = ns
        snames = [x.simplify().__str__() for x in s]
        s2 = []
        for i, x in enumerate(s):
            if Neg(x).nnf().__str__() in snames[i+1:]:
                return Const(False)
            elif isinstance(x, Const):
                if x.value is False:
                    return Const(False)
            elif snames[i] not in snames[i+1:]:
                s2.append(x)

        if len(s2) < 1:
            return Const(True)
        elif len(s2) is 1:
            return s2[0]
        return And(s2)

    def cnf(self):
        return And([x.cnf().simplify() for x in self.value])

    def length(self):
        return sum([x.length() for x in self.value])


class Or():
    """
    Or operator
    """

    def __init__(self, lst):
        self.value = lst

    def __str__(self):
        s = "("
        for i in self.value:
            s += str(i)+" | "
        s = s[:len(s)-3]
        return s + ")"

    def solve(self, v):
        for l in self.value:
            if l.solve(v) is True:
                return True
        return False

    def simplify_cnf(self, v):
        return Or([x.simplify_cnf(v) for x in self.value])

    def nnf(self):
        return Or([x.nnf() for x in self.value])

    def simplify(self):
        s = [x.simplify() for x in self.value]
        # Or list flatten
        ns = []
        for x in s:
            if isinstance(x,Or):
                ns.extend(x.value)
            else:
                ns.append(x)
        s = ns
        snames = [x.simplify().__str__() for x in s]
        s2 = []
        for i, x in enumerate(s):
            if Neg(x).nnf().__str__() in snames[i+1:]:
                return Const(True)
            elif isinstance(x, Const):
                if x.value is True:
                    return Const(True)
            elif snames[i] not in snames[i+1:]:
                s2.append(x)

        if len(s2) < 1:
            return Const(False)
        elif len(s2) is 1:
            return s2[0]
        return Or(s2)

    def cnf(self):
        s = [x.cnf().simplify() for x in self.value]
        s1 = [x.value if isinstance(x, And) else [x] for x in s]
        s2 = []
        for e in itertools.product(*s1):
            s3 = []
            for x in e:
                if isinstance(x,Or):
                    s3.extend(x.value)
                else:
                    s3.append(x)
            s2.append(Or(s3))
        if len(s2) is 1:
            return s2[0]
        return And(s2)

    def length(self):
        return sum([x.length() for x in self.value])


class Const():
    """
    Constant
    """

    def __init__(self, c):
        self.value = c

    def __str__(self):
        return str(self.value)

    def solve(self, v):
        return self.value

    def simplify_cnf(self, v):
        return self

    def nnf(self):
        return self

    def negate(self):
        if self.value is True:
            return Const(False)
        return Const(True)

    def simplify(self):
        return self

    def cnf(self):
        return self

    def length(self):
        return 1
