import sys

from vepar import Memorija
from SnailParser import P


def izvrsi(src: str):
    mem = Memorija(redefinicija=False)
    program, fje = P(src)
    program.izvrsi(mem, unutar=None)

"""
Pozicionirati se u direktorij 'snailang'.
Primjer pokretanja:
$ python3 src/Snail.py examples/faktorijel.snail
"""
if __name__ == '__main__':
    with open(sys.argv[1]) as src_file:
        izvrsi(src_file.read())