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

    def stmt_list(p) -> '(assign|print|input|if|fun|ret|fn_call)*':
        lista = []
        while ...:        
            if p > T.IME: lista.append(p.assign())
            elif p > T.PRINT: lista.append(p.print())
            elif p > T.INPUT: lista.append(p.input())
            elif p > T.IF: lista.append(p.cond())
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
    
    def cond(p):
        p >> T.IF
        value = p.expr()
        p >> T.THEN
        then = p.stmt_list()
        instead = []        
        if p >= T.ELSE:
            instead = p.stmt_list()
        return If( value, then, instead )

    def param_list():
        lista = []
        if p > T.IME:      
            while t := p >> T.IME:
                lista.append(t)
                if p >= T.ZAREZ: continue            
                else: break
        # ovdje bi trebalo baciti gresku ako je prvo sto vidi obicni zarez
        return lista        

    def fun(p):
        p >> T.FUN
        name = p >> T.IME
        p >> T.OOTV
        args = p.param_list()
        p >> T.OZATV
        p >> T.DVOTOCKA
        do = p.stmt_list()
        p >> T.ENDFUN        
        return Function( name, args, do )        
        
    def ret(p):
        p >> T.RETURN
        what = p.expr()
        return Return( what )

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
    instead: 'stmt*'

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
    operator: '-' 
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
