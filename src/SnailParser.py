from AbstractSnailTree import *
from SnailTokens import T
from SnailLexer import snail


### BKG
# program -> stmt_list
# stmt_list -> stmt_list stmt
#            | stmt
# stmt -> assign | print | input | random | cond | fun | ret
# assign -> IME PRIDRUZI expr TOCKAZ
# print -> PRINT NEWLINE TOCKAZ | PRINT expr TOCKAZ
# input -> INPUT IME TOCKAZ
# random -> RANDOM BROJ MANJEJ IME MANJE BROJ TOCKAZ
# cond -> IF expr THEN stmt_list (ELSE stmt_list)? ENDIF
# fun -> FUN IME OOTV param_list OZATV DVOTOCKA stmt_list ENDFUN
# param_list -> '' | IME | param_list ZAREZ IME
# ret -> RETURN expr
# fn_call -> IME OOTV arg_list OZATV
# arg_list -> '' | expr | arg_list ZAREZ expr
class P(Parser):
    namef = None
    paramsf = None

    def program(p):
        p.funkcije = Memorija(redefinicija=False)
        return Program(p.stmt_list()), p.funkcije

    def stmt_list(p) -> "[stmt]":
        stmts = []
        while ...:
            if p > T.PRINT:
                stmts.append(p.print())
                p >> T.TOCKAZAREZ
            elif p > T.INPUT:
                stmts.append(p.input())
                p >> T.TOCKAZAREZ
            elif p > T.RANDOM:
                stmts.append(p.random())
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

    def assign(p) -> Assign:
        ime = p >> T.IME
        p >> T.PRIDRUZI
        izraz = p.expr()
        return Assign(ime, izraz)
    
    def print(p) -> Print:
        p >> T.PRINT
        if what := p >= T.NEWLINE:
            return Print(what)
        else: 
            what = p.expr()
            return Print(what)

    def input(p) -> Input:
        p >> T.INPUT
        ime = p >> T.IME
        return Input(ime)

    def random(p) -> Random:
        p >> T.RANDOM
        od = p >> T.BROJ
        p >> T.MANJEJ
        ime = p >> T.IME
        p >> T.MANJE
        do = p >> T.BROJ
        return Random(ime, od, do)

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
        
    def ret(p) -> Return:
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
