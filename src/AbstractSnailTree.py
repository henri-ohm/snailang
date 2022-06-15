from vepar import *
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


class Assign(AST):
    ime: 'IME'
    izraz: 'expr'


class Print(AST):
    what: 'expr|STRING|NEWLINE'


class Input(AST):
    variable: 'IME'


class If(AST):
    value: 'expr'
    then: 'stmt*'
    instead: 'stmt*'


class Function(AST):
    name: 'IME'
    parameters: 'IME*'
    body: 'stmt*'


class Return(AST):
    what: 'expr'


class Binary(AST):
    operator:'+|-|*|/'
    left: 'IME|BROJ'
    right: 'IME|BROJ'


class Unary(AST):
    operator: '-'
    right: 'IME|BROJ'


class Comparison(AST):
    operator: '<|>|<=|>=|==|!='
    left: 'IME|BROJ'
    right: 'IME|BROJ'


class FunctionCall(AST):
    name: 'IME'
    args: 'IME*'