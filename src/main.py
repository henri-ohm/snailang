from vepar import *

class T(TipoviTokena):
    PLUS, MINUS, PUTA, PODIJELJENO = '+-*/'
    MANJE, VISE, MANJEJ, VISEJ = '<', '>', '<=', '>='
    JJEDNAKO, RAZLICITO = '==', '!='
    PRIDRUZI, PRINT, NEWLINE, TOCKAZAREZ = '=', 'print', 'newline', ';'    
    IF, THEN, ELSE, ENDIF, OOTV, OZATV = 'if', 'then', 'else', 'endif', '(', ')'
    FUN, ENDFUN, RETURN = 'fun', 'endfun', 'return'
    INPUT = 'input'

    
    class BROJ(Token): pass
    class IME(Token):pass
    class STRING(Token): pass

@lexer
def snail(lex):
    for znak in lex:
        if znak.isspace():
            lex.zanemari()
        elif znak.isalpha():
            lex * str.isalnum
            yield lex.literal_ili(T.IME)
        elif znak.isdecimal():
            lex.prirodni_broj(znak)
            yield lex.token(T.BROJ)
        elif znak == '"':
            lex - '"'
            yield lex.token(T.STRING)
        elif znak == '/':
            if lex >= '*':
                while True:
                    lex.pročitaj_do('*', više_redova = True)
                    if(lex >= '/'): break
            elif lex >= '/':
                lex - '\n'
            else:
                yield lex.token(T.PODIJELJENO)                
            lex.zanemari()
        else:
            lex.literal(T)


snail('''
print newline;
''')
snail('''
print i*i; // print the square of i
if i == v/2 then // is i the half of v?
print newline; //yes
else
print "--"; //no
endif
''')
