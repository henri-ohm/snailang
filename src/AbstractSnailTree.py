from vepar import *
from SnailTokens import T
from math import ceil
from random import randrange
### AST
# Program: stmt_list: [stmt]
# stmt: Assign: name:IME assigned: expr
#       Print: what:expr|NEWLINE
#       Input: where:IME
#       If: cond:expr then:[stmt] else:[stmt]
#       Function: name:IME params:[IME] body: [stmt]
#       Return: what:expr
# expr: Binary: op:+|-|*|/ l:expr r:expr
#       Unary: op:- r:expr
#       Comp: rel:<|>|<=|>=|==|!=
#       FunctionCall: name:IME args:[expr]
#       IME|BROJ


class Program(AST):
    stmt_list: "[stmt]"
    def izvrsi(self, mem, unutar):
        for stmt in self.stmt_list:
            stmt.izvrsi(mem, unutar)


class Assign(AST):
    ime: 'IME'
    izraz: 'expr'
    def izvrsi(self, mem, unutar):
        mem[self.ime] = self.izraz.vrijednost(mem, unutar)


class Print(AST):
    what: 'expr|NEWLINE'
    def izvrsi(self, mem, unutar):
        if self.what ^ T.NEWLINE:
            print()
        else:
            print(self.what.vrijednost(mem, unutar), end='')


class Input(AST):
    variable: 'IME'
    def izvrsi(self, mem, unutar):
        inp = input()
        try:
            inp = int(inp)
        except:
            ...
        mem[self.variable] = inp


class Random(AST):
    ime: 'IME'
    od: 'expr'
    do: 'expr'
    def izvrsi(self, mem, unutar):
        l = self.od.vrijednost(mem, unutar)
        r = self.do.vrijednost(mem, unutar)
        mem[self.ime] = randrange(start=l, stop=r)


class If(AST):
    value: 'expr'
    then: '[stmt]'
    instead: '[stmt]'
    def izvrsi(self, mem, unutar):
        vr = self.value.vrijednost(mem, unutar)
        stmts = self.then if vr else self.instead
        for s in stmts:
            s.izvrsi(mem, unutar)


class Function(AST):
    name: 'IME'
    parameters: 'IME*'
    body: '[stmt]'
    def izvrsi(self, mem, unutar):
        ...
    def pozovi(self, arguments):
        local_params = Memorija(zip(self.parameters, arguments))
        try:
            for stmt in self.body:
                stmt.izvrsi(mem=local_params, unutar=self)
        except Povratak as e: return e.preneseno
        else: raise GreškaIzvođenja(f'{self.name} nije ništa vratila')

class FunctionCall(AST):
    name: 'IME'
    args: 'IME*'
    def vrijednost(self, mem, unutar):
        fn_name = self.name
        if fn_name is nenavedeno:
            fn_name = unutar
        argumenti = [a.vrijednost(mem, unutar) for a in self.args]
        return fn_name.pozovi(argumenti)

class Return(AST):
    what: 'expr'
    def izvrsi(self, mem, unutar):
        raise Povratak(self.what.vrijednost(mem, unutar)) # PAZI: return izvan funkcije je semanticka pogreska

class Binary(AST):
    op: '+|-|*|/'
    left: 'expr'
    right: 'expr'
    def vrijednost(self, mem, unutar):
        x = self.left.vrijednost(mem, unutar)
        y = self.right.vrijednost(mem, unutar)
        
        #jedino plus implementiramo za sve tokene
        #za stringove je plus konkatenacija
        if self.left ^ T.STRING and self.right ^ T.STRING: return x + y

        if self.left ^ T.STRING:
            x = len(self.left.vrijednost(mem, unutar))
        if self.right ^ T.STRING:
            y = len(self.right.vrijednost(mem, unutar))

        speedToNumber = { 's': -1, 'n': 0, 'f': 1}
        numberToSpeed = {-1: 's', 0: 'n', 1: 'f'}
        if self.right ^ T.SPEED:
            y = speedToNumber[self.right.vrijednost(mem, unutar)]
        if self.left ^ T.SPEED:
            x = speedToNumber[self.left.vrijednost(mem, unutar)]
        
        if self.left ^ T.SPEED and self.right ^ T.SPEED:
            return numberToSpeed[((x + y)/2)]


        if self.op ^ T.PLUS: return x + y
        elif self.op ^ T.MINUS: return x - y
        elif self.op ^ T.PUTA: return x * y
        elif self.op ^ T.PODIJELJENO: return x // y


class Unary(AST):
    operator: '+-'
    right: 'expr'
    def vrijednost(self, mem, unutar):
        rval = self.right.vrijednost(mem, unutar)
        if self.right ^ T.SPEED:
            if self.operator ^ T.PLUS:
                return {
                    's': 'n',
                    'n': 'f',
                    'f': 'f'
                }[self.right.vrijednost(mem, unutar)]
            else:
                return {
                    's': 's',
                    'n': 's',
                    'f': 'n'
                }[self.right.vrijednost(mem, unutar)]
        elif self.right ^ T.STRING:
            return rval if self.operator ^ T.PLUS else rval[::-1]

        return rval if self.operator ^ T.PLUS else -rval


class Comparison(AST):
    op: '<|>|<=|>=|==|!='
    left: 'expr'
    right: 'expr'
    def vrijednost(self, mem, unutar):
        x = self.left.vrijednost(mem, unutar)
        y = self.right.vrijednost(mem, unutar)
        res = 0

        if (self.left ^ {T.STRING, T.SPEED} or self.right ^ {T.STRING, T.SPEED}): 
            if type(self.left) != type(self.right): return 0
            if self.left.vrijednost(mem, unutar) == self.right.vrijednost(mem, unutar): return 1

        if self.op ^ T.MANJE:
            res = x < y
        elif self.op ^ T.MANJEJ:
            res = x <= y
        elif self.op ^ T.VISE:
            res = x > y
        elif self.op ^ T.VISEJ:
            res = x >= y
        elif self.op ^ T.JJEDNAKO:
            res = x == y
        elif self.op ^ T.RAZLICITO:
            res = x != y

        return res

class Ternary(AST):
    first: 'expr'
    second: 'expr'
    third: 'expr'

    def vrijednost(self, mem, unutar):
        x = self.first.vrijednost(mem, unutar)
        y = self.second.vrijednost(mem, unutar)
        z = self.third.vrijednost(mem, unutar)
        return y if x else z



class Povratak(NelokalnaKontrolaToka): """Povratak iz funkcije."""