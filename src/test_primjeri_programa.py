pr_print = """
print x;
print 1+2;
print newline;
"""

pr_input = """
input x;
"""

pr_expr = """
a = (a + 3) + 2 / 3 - 4 * 4;
b = 3 < 2;
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