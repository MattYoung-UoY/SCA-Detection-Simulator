from typing import Callable

def generate_dataset(probDistPattern: list[tuple[Callable[[float], int], int]]):
    result = []
    actual_means = []

    totalSamples = 0
    for probDist in probDistPattern:
        totalSamples += probDist[1]
    
    for probDist in probDistPattern:
        for samples in range(probDist[1]):
            probDistResult = probDist[0](0)
            actual_means.append(probDistResult[0])
            result.append(probDistResult[1])

    return (actual_means, result)