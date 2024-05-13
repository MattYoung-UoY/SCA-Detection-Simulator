import math

def chernoff_hoeffding_bound(delta_p: float, epsilon: float):
    return math.ceil(math.log(2/epsilon)/(2*(delta_p**2)))