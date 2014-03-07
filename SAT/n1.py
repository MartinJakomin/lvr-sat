__author__ = 'Martin Jakomin'


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

class Var():
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return self.name

    def solve(self,v):
        return v[self.name]

    def nnf(self):
        return self.name
        

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
        

class Const():
    def __init__(self,c):
        self.value = c

    def __str__(self):
        return (str(self.value))

    def solve(self,v):
        return self.value

    def nnf(self):
        return self.value

    def negate(self):
        if self.value is True:
            return False
        return True

    

def solve(f,v):
    return f.solve(v)

def nnf(f):
    return f.nnf()


"""
a = Var("p")
b = Neg(a)

print(b)

d = Const(True)
c = Or([a,b,d])
print(c)

print 
print(solve(And([Var("p"),Neg(Var("p"))]),{"p":True}))
print(solve(Neg(Or([Var("p"), And([Or([Neg(Var("p")), Var("q")]), Neg(Var("q"))])])),{"p":False, "q":True}))

print
print(nnf(Neg(And([Var("p"),Var("p"),Const(True)]))))
print(nnf(Neg(Neg(Neg(Neg(Or([Var("p"), And([Or([Neg(Var("p")), Var("q")]), Neg(Var("q"))])])))))))
"""

#TODO: Poenostavljanje izraza
