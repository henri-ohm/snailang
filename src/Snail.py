import sys

from vepar import Memorija, prikaz
from SnailParser import P
from SnailLexer import snail


def izvrsi(src: str):
    mem = Memorija(redefinicija=False)
    program, fje = P(src)
    program.izvrsi(mem, unutar=None)

"""
Pozicionirati se u direktorij 'snailang'.
Primjer pokretanja:
$ python3 src/Snail.py examples/07-faktorijel.snail
"""
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python3 src/Snail.py SRC [-v] ")
    with open(sys.argv[1]) as src_file:
        src = src_file.read()

        if len(sys.argv) == 3 and sys.argv[2] == "-v":
            print("-----------------LEX---------------")
            print(snail(src))
            print("----------------PARSE--------------")
            print(prikaz(P(src)))
            print("----------------EXEC---------------")
        izvrsi(src)
