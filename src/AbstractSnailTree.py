from vepar import *
from src.SnailTokens import T
### AST
# Program: stmt_list: [stmt]
# stmt: Assign: name:IME assigned: expr
#       Print: what:expr|STRING|NEWLINE
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
    def izvrsi(self, mem):
        for stmt in self.stmt_list:
            stmt.izvrsi(mem)


class Assign(AST):
    ime: 'IME'
    izraz: 'expr'
    def izvrsi(self, mem):
        mem[self.ime] = self.izraz.vrijednost(mem)



class Print(AST):
    what: 'expr|STRING|NEWLINE'
    def izvrsi(self, mem):
        if self.what ^ T.NEWLINE:
            print()
        else:
            print(self.what.vrijednost(mem), end='')


class Input(AST):
    variable: 'IME'
    def izvrsi(self, mem):
        inp = input()
        try:
            inp = int(inp)
        except:
            ...
        mem[self.variable] = inp


class If(AST):
    value: 'expr'
    then: '[stmt]'
    instead: '[stmt]'
    def izvrsi(self, mem):
        vr = self.value.vrijednost(mem)
        stmts = self.then if vr else self.instead
        for s in stmts:
            s.izvrsi(mem)


class Function(AST):
    name: 'IME'
    parameters: 'IME*'
    body: 'stmt*'
    def izvrsi(self, mem):
        # TODO
        pass


class Return(AST):
    what: 'expr'
    def izvrsi(self, mem):
        # TODO
        pass

class Binary(AST):
    op: '+|-|*|/'
    left: 'expr'
    right: 'expr'
    def vrijednost(self, mem):
        x = self.left.vrijednost(mem)
        y = self.right.vrijednost(mem)
        if self.op ^ T.PLUS: return x + y
        elif self.op ^ T.MINUS: return x - y
        elif self.op ^ T.PUTA: return x * y
        elif self.op ^ T.PODIJELJENO: return x // y


class Unary(AST):
    operator: '-'
    right: 'expr'
    def vrijednost(self, mem):
        rval = self.right.vrijednost(mem)
        return -rval


class Comparison(AST):
    op: '<|>|<=|>=|==|!='
    left: 'expr'
    right: 'expr'
    def vrijednost(self, mem):
        x = self.left.vrijednost(mem)
        y = self.right.vrijednost(mem)
        res = 0

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


class FunctionCall(AST):
    name: 'IME'
    args: 'IME*'
    def izvrsi(self, mem):
        # TODO
        pass