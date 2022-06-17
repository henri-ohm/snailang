from AbstractSnailTree import *
from SnailTokens import T


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
        elif znak == '^':
            lex >> {'s', 'n', 'f'}
            lex >> '^'
            yield lex.token(T.SPEED)
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


### BKG
# program -> stmt_list
# stmt_list -> stmt_list stmt TOCKAZ
#            | stmt TOCKAZ
# stmt -> assign | print | input | cond | fun | ret
# assign -> IME PRIDRUZI expr
# print -> PRINT NEWLINE | PRINT expr
# input -> INPUT IME
# cond -> IF expr THEN stmt_list (ELSE stmt_list)? ENDIF
# fun -> FUN IME OOTV param_list OZATV DVOTOCKA stmt_list ENDFUN
# param_list -> '' | IME | param_list ZAREZ IME
# ret -> RETURN expr
# fn_call -> IME OOTV arg_list OZATV
# arg_list -> (IME|BROJ)*
class P(Parser):
    namef=None
    paramsf=None

    def program(p):
        p.funkcije = Memorija(redefinicija=False)
        return Program(p.stmt_list()), p.funkcije

    def stmt_list(p) -> "Program":
        stmts = []
        while ...:
            if p > T.PRINT:
                stmts.append(p.print())
                p >> T.TOCKAZAREZ
            elif p > T.INPUT:
                stmts.append(p.input())
                p >> T.TOCKAZAREZ
            elif p > T.IF:
                stmts.append(p.cond())
            elif p > T.FUN:
                function = p.fun()
                stmts.append(function)
                p.funkcije[function.name] = function
            elif p > T.RETURN:
                stmts.append(p.ret())
                p >> T.TOCKAZAREZ
            elif p > T.IME:
                stmts.append(p.assign())
                p >> T.TOCKAZAREZ
            else:
                break

        return stmts

    def assign(p) -> "Assign":
        ime = p >> T.IME
        p >> T.PRIDRUZI
        izraz = p.expr()
        return Assign(ime, izraz)
    
    def print(p) -> "Print":
        p >> T.PRINT
        if what := p >= T.NEWLINE:
            return Print(what)
        else: 
            what = p.expr()
            return Print(what)

    def input(p) -> "Input":
        p >> T.INPUT
        ime = p >> T.IME
        return Input(ime)
    
    def cond(p) -> "If":
        p >> T.IF
        value = p.expr()
        p >> T.THEN
        then = p.stmt_list()
        instead = []        
        if p >= T.ELSE:
            instead = p.stmt_list()
        p >> T.ENDIF
        return If(value, then, instead)

    def fun(p) -> "Function":
        p >> T.FUN
        p.namef = name = p >> T.IME
        p >> T.OOTV
        p.paramsf = params = p.param_list()
        p >> T.OZATV
        p >> T.DVOTOCKA
        do = p.stmt_list()
        p >> T.ENDFUN
        return Function(name, params, do)

    def param_list(p) -> "[T.IME]":
        params = []

        while ime := p >= T.IME:
            params.append(ime)
            if not p >= T.ZAREZ:
                break

        return params
        
    def ret(p) -> "Return":
        p >> T.RETURN
        what = p.expr()
        return Return(what)
    
    def name_or_fn_call(p, name) -> "T.IME|FunctionCall":
        if name in p.funkcije:
            function = p.funkcije[name]
            return FunctionCall(function, p.argument_list(function.parameters))
        elif name == p.namef:
            return FunctionCall(nenavedeno, p.argument_list(p.paramsf))
        else:
            return name

    def argument_list(p, params):
        args = []
        p >> T.OOTV
        for i, _ in enumerate(params):
            if i:
                p >> T.ZAREZ
            args.append(p.expr())
        p >> T.OZATV
        return args

    def expr(p):
        if op := p >= {T.PLUS, T.MINUS}:
            inside = p.expr()
            return Unary(op, inside)
        else:
            left = None
            if p >= T.OOTV:
                left = p.expr()
                p >> T.OZATV
            elif p > T.BROJ:
                left = p >> T.BROJ
            elif left := p >= T.IME:
                left = p.name_or_fn_call(left)
            elif p > T.STRING:
                left = p >> T.STRING
            elif p > T.SPEED:
                left = p >> T.SPEED
            

            if op := p >= {T.PLUS, T.MINUS, T.PUTA, T.PODIJELJENO}:
                right = p.expr()
                if (left ^ {T.STRING, T.SPEED} or right ^ {T.STRING, T.SPEED}) and op ^ {T.MINUS, T.PUTA, T.PODIJELJENO}: 
                    raise SintaksnaGreška(op, " nije definirana operacija za ", left, "i", right )
                
                return Binary(op, left, right)
            elif op := p >= {T.MANJE, T.VISE, T.MANJEJ, T.VISEJ, T.JJEDNAKO, T.RAZLICITO}:
                right = p.expr()
                if (left ^ {T.STRING, T.SPEED} or right ^ {T.STRING, T.SPEED}) and op ^ {T.MANJE, T.VISE, T.MANJEJ, T.VISEJ}: 
                    raise SintaksnaGreška(op, " nije definirana operacija za ", left, "i", right )
                
                return Comparison(op, left, right)

            if p >= T.HESTEG:
                first = p.expr()
                p >> T.UPITNIK
                second = p.expr()
                p >> T.UPITNIK
                third = p.expr()
                p >> T.UPITNIK
                return Ternary(first, second, third)
            return left
