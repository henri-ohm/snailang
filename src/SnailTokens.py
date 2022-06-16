from vepar import TipoviTokena, Token


class T(TipoviTokena):
    PLUS, MINUS, PUTA, PODIJELJENO, MANJE, VISE, PRIDRUZI, ZAREZ, TOCKAZAREZ, DVOTOCKA, OOTV, OZATV = '+-*/<>=,;:()'
    MANJEJ, VISEJ, JJEDNAKO, RAZLICITO = '<=', '>=', '==', '!='
    PRINT, NEWLINE, INPUT = 'print', 'newline', 'input'
    IF, THEN, ELSE, ENDIF = 'if', 'then', 'else', 'endif'
    FUN, ENDFUN, RETURN = 'fun', 'endfun', 'return'

    class BROJ(Token):
        def vrijednost(self, mem, unutar):
            return int(self.sadržaj)

    class IME(Token):
        def vrijednost(self, mem, unutar):
            return mem[self]

    class STRING(Token):
        def vrijednost(self, mem, unutar):
            return self.sadržaj[1:-1]
