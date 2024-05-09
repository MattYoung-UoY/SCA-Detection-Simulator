import sampleGenerator
import random

def const0(t:float):
    return 0

def const1(t:float):
    return 1

def equalProb(t:float):
    return random.randint(0, 1)

probDistPattern = [(const0, 5), (const1, 5), (equalProb,10)]

samples = sampleGenerator.generateSamples(probDistPattern);

print(samples)