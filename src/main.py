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

''')
