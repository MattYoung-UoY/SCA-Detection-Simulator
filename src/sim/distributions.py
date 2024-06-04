import random

def const_0(t:float):
    return (0, 0)

def const_1(t:float):
    return (1, 1)

def uniform_dist(t:float):
    return (0.5, random.randint(0, 1))

def quarter_mean(t:float):
    return (0.25, 0) if random.random() < 0.75 else (0.25, 1)

def three_quarter_mean(t:float):
    return (0.75, 0) if random.random() < 0.25 else (0.75, 1)