__author__ = 'Martin Jakomin & Mateja Rojko'

import itertools


class Neg():
    def __init__(self,v):
        self.value = v

    def __str__(self):
        return "~" + str(self.value.__str__())

    def solve(self,v):
        return not(self.value.solve(v))

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



class Var():
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return self.name

    def solve(self,v):
        return v[self.name]

    def nnf(self):
        return self

    def simplify(self):
        return self

    def cnf(self):
        return self

class And():
    def __init__(self,lst):
        self.value = lst

    def __str__(self):
        s = "("
        for i in self.value:
            s += str(i)+" & "
        s = s[:len(s)-3]
        return s + ")"

    def solve(self,v):
        for l in self.value:
            if l.solve(v) is False:
                return False
        return True

    def nnf(self):
        return And([x.nnf() for x in self.value])

    def simplify(self):
        s = [x.simplify() for x in self.value]
        snames = [x.simplify().__str__() for x in self.value]
        s2 = []
        for i,x in enumerate(s):
            if Neg(x).nnf().__str__() in snames[i+1:]:
                return Const(False)
            elif isinstance(x,Const):
                if x.value is False:
                    return Const(False)
            elif snames[i] not in snames[i+1:]:
                s2.append(x)
        return And(s2)

    def cnf(self):
        return And([x.cnf() for x in self.value])


class Or():
    def __init__(self,lst):
        self.value = lst

    def __str__(self):
        s = "("
        for i in self.value:
            s += str(i)+" | "        
        s = s[:len(s)-3]
        return s + ")"

    def solve(self,v):
        for l in self.value:
            if l.solve(v) is True:
                return True
        return False

    def nnf(self):
        return Or([x.nnf() for x in self.value])

    def simplify(self):
        s = [x.simplify() for x in self.value]
        snames = [x.simplify().__str__() for x in self.value]
        s2 = []
        for i,x in enumerate(s):
            if Neg(x).nnf().__str__() in snames[i+1:]:
                return Const(True)
            elif isinstance(x,Const):
                if x.value is True:
                    return Const(True)
            elif snames[i] not in snames[i+1:]:
                s2.append(x)
        return Or(s2)

    def cnf(self):
        s = [x.cnf() for x in self.value]
        s1 = [x.value if isinstance(x, And) else [x] for x in s]
        s2 = []
        print "----"
        for e in itertools.product(*s1):
            #s2.append(Or([x for x in e]))
            print e[0],e[1].__class__, e[1]
            s3 = []
            for x in e:
                if isinstance(x, Or):
                    print "asd"
                    pass
                else:
                    s3.append(x)
            s2.append(Or(s3))

        #TODO: Debug
        print And(s2).value
        return And(s2)


class Const():
    def __init__(self,c):
        self.value = c

    def __str__(self):
        return (str(self.value))

    def solve(self,v):
        return self.value

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


def solve(f,v):
    return f.solve(v)


def nnf(f):
    return f.nnf()


def simplify(f):
    return nnf(f).simplify()


def cnf(f):
    print f
    return nnf(f).cnf()

#print simplify(Neg(And([Var("p"),Var("p"),Var("q"),Var("p"),Neg(Var("p1")),Const(True)])))


print cnf(Or([Var("x"),And([Var("y"),Var("s"),Or([Var("g"),Var("s")])])]))