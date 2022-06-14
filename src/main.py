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
            if p > T.PRINT: lista.append(p.print())
            elif p > T.INPUT: lista.append(p.input())
            elif p > T.IF: lista.append(p.cond())
            elif p > T.FUN: lista.append(p.fun())
            elif p > T.RETURN: lista.append(p.ret())
            elif name := p >= T.IME: 
                if p > T.PRIDRUZI:                
                    lista.append( p.assign( name ) )      
                elif p > T.OOTV:
                    lista.append( p.function_call( name ) )      
            else: return lista

    def assign(p, name):
        left = name
        p >> T.PRIDRUZI
        right = p.expr()
        p >> T.TOCKAZAREZ
        return Assign(left, right)
    
    def print(p):
        p >> T.PRINT
        if what := p >= {T.STRING, T.NEWLINE}:
            p >> T.TOCKAZAREZ
            return Print( what )
        else: 
            what = p.expr()
            p >> T.TOCKAZAREZ
            return Print( what )

    def input(p):
        p >> T.INPUT
        variable = p >> T.IME
        p >> T.TOCKAZAREZ
        return Input( variable )
    
    def cond(p):
        p >> T.IF
        value = p.expr()
        p >> T.THEN
        then = p.stmt_list()
        instead = []        
        if p >= T.ELSE:
            instead = p.stmt_list()
        p >> T.ENDIF
        return If( value, then, instead )

    def param_list(p):
        lista = []
        p >> T.OOTV

        while True:
            t = p.expr()
            lista.append( t )
            if p >= T.ZAREZ: continue            
            else: break

        p >> T.OZATV
        return lista        

    def fun(p):
        p >> T.FUN
        name = p >> T.IME
        args = p.param_list()
        p >> T.DVOTOCKA
        do = p.stmt_list()
        p >> T.ENDFUN        
        return Function( name, args, do )        
        
    def ret(p):
        p >> T.RETURN
        what = p.expr()
        return Return( what )
    
    def function_call(p, name):
        args = p.param_list()
        p >> T.TOCKAZAREZ
        return FunctionCall( name, args )

    def expr(p):
        if( operator := p >= T.MINUS ):
            right = p.expr()
            return Unary( operator, right )
        else:
            left = p >> {T.IME, T.BROJ}
            if operator := p >= {T.PLUS, T.MINUS, T.PUTA, T.PODIJELJENO}:
                right = p.expr()
                return Binary(left, operator, right)
            elif operator := p >= {T.MANJE, T.VISE, T.MANJEJ, T.VISEJ, T.JJEDNAKO, T.RAZLICITO}:
                right = p.expr()
                return Comparison( left, operator, right )
            
            if left ^ T.IME: return Number( left )            
            elif left ^ T.BROJ: return Variable( left )

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

class Variable(AST):
    name: 'IME'

class Number(AST):
    num: 'BROJ'



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

ast = P('''
fun fib(x, y):
    ~ ova funkcija racuna fibonacijeve brojeve
    i pise ih u beskonacnost ~
    print x;
    print newline;
    fib(y, x+y);
endfun
x = 1/1; 
fib(x,x);
if x >= 0 then 
    x = 1;
else
    x = 2;
endif
''')

prikaz(ast)
