from vepar import *


class T(TipoviTokena):
    PLUS, MINUS, PUTA, PODIJELJENO, MANJE, VISE, PRIDRUZI, ZAREZ, TOCKAZAREZ, DVOTOCKA, OOTV, OZATV = '+-*/<>=,;:()'
    MANJEJ, VISEJ, JJEDNAKO, RAZLICITO = '<=', '>=', '==', '!='
    PRINT, NEWLINE, INPUT = 'print', 'newline', 'input'
    IF, THEN, ELSE, ENDIF = 'if', 'then', 'else', 'endif'
    FUN, ENDFUN, RETURN = 'fun', 'endfun', 'return'

    class BROJ(Token):
        pass
    class IME(Token):
        pass
    class STRING(Token):
        pass


@lexer
def snail(lex):
    for znak in lex:
        if znak.isspace():
            lex.zanemari()
        elif znak == '<':
            yield lex.token(T.MANJEJ if lex >= '=' else T.MANJE)
        elif znak == '>':
            yield lex.token(T.VISEJ if lex >= '=' else T.VISE)
        elif znak == '=':
            yield lex.token(T.JJEDNAKO if lex >= '=' else T.PRIDRUZI)
        elif znak == '!':
            lex >> '='
            lex.token(T.RAZLICITO)
        elif znak.isalpha():
            lex * str.isalnum
            yield lex.literal_ili(T.IME)
        elif znak.isdecimal():
            lex.prirodni_broj(znak)
            yield lex.token(T.BROJ)
        elif znak == '"':
            lex - '"'
            yield lex.token(T.STRING)
        elif znak == "~":
            lex.pročitaj_do("~", više_redova=True)
            lex.zanemari()
        elif znak == '/':
            if lex >= '/':
                lex - '\n'
                lex.zanemari()
            else:
                yield lex.token(T.PODIJELJENO)
        else:
            yield lex.literal(T)


class P(Parser):
    def program(p) -> 'Program': return Program(p.stmt_list())

    def stmt_list -> '(assign|print|input|if|fun|ret|fn_call)*':
        lista = []
        while ...:        
            if p > T.IME: lista.append(p.assign())
            elif p > T.PRINT: lista.append(p.print())
            elif p > T.INPUT: lista.append(p.input())
            elif p > T.IF: lista.append(p.if())
            elif p > T.FUN: lista.append(p.fun())
            elif p > T.RET: lista.append(p.ret())
            else: return lista

    def assign(p):
        left = p >> T.IME
        p >> T.PRIDRUZI
        right = p.expr()
        return Assign(left, right)
    
    def print(p):
        p >> T.PRINT
        if what := p >= {T.STRING, T.NEWLINE}: 
            return Print( what )
        else: 
            what = p.expr()
            return Print( what )

    def input(p):
        p >> T.INPUT
        variable = p >> T.IME
        return Input( variable )
    def if(p):
    def fun(p):
    def ret(p):

class Program(AST):
    stmt_list: 'stmt*'

class Assign(AST):
    left: 'IME'
    right: 'expr'

class Print(AST):
    what: 'expr|STRING|NEWLINE'
    
class Input(AST):
    variable: 'IME'

class If(AST):
    value: 'expr'
    then: 'stmt*'
    else: 'stmt*'

class Function(AST):
    name: 'IME'
    args: 'IME*'
    do: 'stmt*'

class Return(AST):
    what: 'expr'

class Binary(AST):
    operator:'+|-|*|/'
    left: 'expr'
    right: 'expr'

class Unary(AST):
    operator:- 
    right: 'expr'

class Comparison(AST):
    operator: '<|>|<=|>=|==|!='

class FunctionCall(AST):
    name: 'IME'
    args: 'IME*'


snail('''
fun fib(x, y):
    ~ ova funkcija racuna fibonacijeve brojeve
    i pise ih u beskonacnost ~
    print x;
    print newline;
    fib(y, x+y);
endfun

x = 1/1 // postavi x na nula
fib(x,x)

if x >= 0 then
    x = 1
else
    x = 2
endif
''')
