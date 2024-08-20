"""Licensed under the MIT License.
Full license can be found in the "LICENSE" file in the repository root directory.

Copyright (c) 2024 Matt Young

Contains the code used to generate datasets to run simulations against.
"""

# Required for the type hinting
from typing import Callable

""" Uses the specified list of probability distributions to generate a dataset representing a raw key.

Args:
    key_bit_dist_pattern(list[tuple[Callable[[float], int], int]]): A list of tuples, each containing a function that represents a probability distribution to be used to generate raw key bits, and the number of raw key bits to generate using each distribution

Returns:
    A tuple of two lists, the first specifying the mean of the distribution used to generate the corresponding key bit in the second list
"""
def generate_dataset(key_bit_dist_pattern: list[tuple[Callable[[float], int], int]]):
    result = []
    actual_means = [] 

    # For each probability distribution...
    for prob_dist in key_bit_dist_pattern:
        # For each sample required by that distribution...
        for samples in range(prob_dist[1]):
            # Call the provided probability distribution function
            # (the parameter passed to the function is a time value. 
            # This allows for distributions that change over time eg. Sinusoidal, square wave, triangular.
            # This feature is not used yet, and so a value of 0 is passed.)
            probDistResult = prob_dist[0](0)
            actual_means.append(probDistResult[0])
            result.append(probDistResult[1])

    return (actual_means, result)