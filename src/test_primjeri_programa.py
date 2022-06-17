pr_print = """
print "1 + 2 = ";
print 1+2;
print newline;
"""

pr_io = """
print "Program za sumu elemenata.";
print newline;
print "Unesite x i y:";
print newline;
input x;
input y;
print "Suma iznosi: ";
print x + y;
print newline;
"""

pr_assign = """
n = 100;
nkopija = n;
suman = (n*(n+1)) / 2;
print "Suma brojeva od 1 do ";
print n;
print " iznosi ";
print suman;
print newline;
"""

pr_if = """
print "Unesite broj za lutriju: ";
input n;
if n == 1*2*3*4*5 then
    print "Pun pogodak!!";
else
    print "Više sreće drugi put :-D";
endif
print newline;
"""

pr_if2 = """
if 7 == 7 then
    print "7 == 7";
endif
print "evo nas";
print newline;
"""

pr_expr = """
a = (a + 3) + 2 / 3 - 4 * 4;
b = (3 < 2);
"""

pr_fun = """
fun id(n):
    return n;
endfun

print "id(2+2) = ";
print id(2+2);
print newline;
"""

pr_fun_gauss = """
fun sumaDo(n):
    return (n*(n+1))/2;
endfun

print "suma brojeva od 1 do 50 = ";
print sumaDo(50);
print newline;
"""

pr_fun_fakt = """
fun fakt(n):
    print "dobio sam n = ";
    print n; print newline;
    if n == 0 then 
        return 1;
    else 
        return n * fakt(n-1);
    endif
endfun

print fakt(10);
print newline;
"""

pr_fun_even = """
fun even(n):
    if n == 0 then 
        return 1;
    else
        if n == 1 then
            return 0;
        else
            return even(n-2);
        endif
    endif
endfun

print even(123);
print newline;
print even(122);
print newline;
"""

pr_slozeniji = """
fun fakt(n):
    if n == 0 then return 0;
    else return n * fakt(n);
    endif
endfun

print fakt(10);
"""

ackermann = """
fun ackermann(x, y):
    if x == 0 then return y+1; endif
    if y == 0 then return ackermann(x-1, 1); endif
    return ackermann(x-1, ackermann(x, y-1));
endfun

fun printaj(koliko):
    if koliko == 0 then return 0; endif
    print "ackermann(3, "; print koliko; print ") = ";
    print ackermann(3, koliko); print newline;
    return printaj(koliko - 1);
endfun

a = printaj(4); ~za sve iznad 4 python veli: maximum recursion depth exceeded~
"""

pr_speed = """
print +^s^;
print newline;
print ^s^+^f^;
print newline;
print "hehe" + " i jos jednom hehe";
print newline;
print ^s^ + "hehe";
print newline;
print ^s^==^s^;
print newline;
print ^s^=="s"; //treba biti false
print newline;
"""