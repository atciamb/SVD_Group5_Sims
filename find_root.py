def bisection(func, xlow, xupp, xtol= 1e-15, ftol= 1e-20, maxiter=100):
    """"
    This function computes the roots by bisection
    
    Inputs: function, xlow, xupp
    
    Outputs: The zero value
    """
    t=0
    while True:
        xm=(1/2)*(xlow+xupp)
        if func(xm)*func(xlow) < 0.0:
            xupp=xm
        elif func(xm)*func(xlow) > 0.0:
            xlow=xm
        else:
            return(xm)
        if t>= maxiter or (abs(xupp-xlow)<xtol and abs(func(xm))<ftol):
            break
        t+=1
    return(xm)
def newton(func, x0, ftol=1e-15, xtola=1e-10, maxiter=30):
    """ This function computes the root using newtons method
    Ins and Outs:
    Inputs: func, the function and the derivitive of the function as a tuple, x0, a guess for where it is, ftol is the tolerance for how off it can be, xtol is the tolerance of the x, maxiter is the maximum iterations
    Outputs: The roots of the function"""
    t=0
    while True:
        (f, df) = func(x0)
        x0=x0-(f/df)
        if (abs(f/df) <= xtola and abs(f)<ftol) or t>= maxiter :
            break
        t+=1
    return(x0,t)

