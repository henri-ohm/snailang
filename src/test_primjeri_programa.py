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

pr_expr = """
a = (a + 3) + 2 / 3 - 4 * 4;
b = (3 < 2);
"""

pr_return = """
return xyz;
"""

pr_fun = """
fun id(n):
    return n;
endfun
"""

pr_slozeniji = """
fun fakt(n):
    if n == 0 then return 0;
    else return n * fakt(n);
    endif
endfun

print fakt(10);
"""