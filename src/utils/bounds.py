"""Licensed under the MIT License.
Full license can be found in the "LICENSE" file in the repository root directory.

Copyright (c) 2024 Matt Young

Contains function definitions for any bounds required by other modules.
"""

import math

def chernoff_hoeffding_bound(delta_p: float, epsilon: float):
    return math.ceil(math.log(2/epsilon)/(2*(delta_p**2)))