from vepar import *

class T(TipoviTokena):
    PLUS, MINUS, PUTA, PODIJELJENO = '+-*/'
    MANJE, VISE, MANJEJ, VISEJ = '<', '>', '<=', '>='
    JJEDNAKO, RAZLICITO = '==', '!='
    PRIDRUZI, PRINT, NEWLINE, TOCKAZAREZ = '=', 'print', 'newline', ';'    
    IF, THEN, ELSE, ENDIF, OOTV, OZATV = 'if', 'then', 'else', 'endif', '(', ')'
    FUN, ENDFUN, RETURN = 'fun', 'endfun', 'return'
    INPUT = 'input'
    OKOMENT, ZKOMENT = '/*', '*/'

    
    class BROJ(Token): pass
    class IME(Token):pass
    class STRING(Token): pass
    
