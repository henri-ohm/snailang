from test_primjeri_programa import *
from vepar import Memorija
from main import P


def izvrsi(src):
    print("POČINJEM IZVRŠAVANJE")
    mem = Memorija(redefinicija=False)
    program, fje = P(src)
    program.izvrsi(mem, unutar=None)
    print("PROGRAM IZVRŠEN")

#izvrsi(pr_print)
#izvrsi(pr_io)
#izvrsi(pr_assign)
#izvrsi(pr_if)
#izvrsi(pr_if2)
izvrsi(pr_fun)
izvrsi(pr_fun_gauss)
izvrsi(pr_fun_fakt)
izvrsi(pr_fun_even)
izvrsi(ackermann)
izvrsi(pr_speed)
izvrsi(pr_ternarni)