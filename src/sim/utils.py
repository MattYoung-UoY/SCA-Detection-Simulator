import math

def chernoff_hoeffding_bound(delta_p: float, epsilon: float):
    return math.ceil(math.log(2/epsilon)/(2*(delta_p**2)))

def delta_entr(n, eps):
    val = math.log2(n)*math.sqrt((2*math.log10(2/eps))/n)
    return val if (val <= 1 and val >= 0) else math.nan