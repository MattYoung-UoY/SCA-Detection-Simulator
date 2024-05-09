import sampleGenerator
from distributions import *

probDistPattern = [(const0, 5), (const1, 5), (equalProb,10)]

samples = sampleGenerator.generateSamples(probDistPattern);

print(samples)