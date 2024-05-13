from typing import Callable

def generate_dataset(probDistPattern: list[tuple[Callable[[float], int], int]]):
    result = []

    totalSamples = 0
    for probDist in probDistPattern:
        totalSamples += probDist[1]
    
    for probDist in probDistPattern:
        for samples in range(probDist[1]):
            result.append(probDist[0](0))

    return result