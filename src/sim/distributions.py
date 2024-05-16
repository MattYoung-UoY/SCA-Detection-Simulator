import random

def const_0(t:float):
    return 0

def const_1(t:float):
    return 1

def uniform_dist(t:float):
    return random.randint(0, 1)

def quarter_mean(t:float):
    return 0 if random.random() < 0.75 else 1