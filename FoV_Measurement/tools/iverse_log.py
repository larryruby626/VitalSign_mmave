import sympy
def log(y,x):
    return sympy.log(x,y)

x = 100
# flog = log(sympy.E,x)
flog = log(sympy.E,x)

print(flog)