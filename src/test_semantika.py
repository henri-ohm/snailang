from test_primjeri_programa import *
from vepar import Memorija
from main import P


def izvrsi(src):
    print("POČINJEM IZVRŠAVANJE")
    mem = Memorija(redefinicija=False)
    program, fje = P(src)
    program.izvrsi(mem)
    print("PROGRAM IZVRŠEN")

#izvrsi(pr_print)
#izvrsi(pr_io)
izvrsi(pr_assign)
izvrsi(pr_if)