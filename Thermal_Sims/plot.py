#
print("Plot using: x,y,title,x-axis,y-axis,marker type(none, *,o))")
def p(x,y,title="Generic Plot",xl="X-axis",yl="Y-axis",m='',L=None):
    """plots x,y,title xlabel ylabel"""
    import matplotlib.pyplot as plt
    import numpy as np
    plt.plot(x,y,marker=m)
    plt.title('Generic Plot',fontsize=10)
    plt.suptitle(title)
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.grid(True)
    if L is not None:
        plt.axhline(y=L, color='red', linestyle='--', linewidth=2)
    plt.show()
    return None


def p2(x,y,title="Generic Plot",xl="X-axis",yl="Y-axis",y2=None):
    """plots x,y,title xlabel ylabel, then x2"""
    import matplotlib.pyplot as plt
    plt.plot(x,y,color='blue',alpha=0.7)
    plt.title(title)
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.grid(True)
    if y2 is None:
        plt.show()
        return None
    else:
        plt.plot(x,y2,color='red',linewidth=2)
        plt.grid(True)
        plt.show()
    return None

