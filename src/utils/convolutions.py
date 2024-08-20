"""Licensed under the MIT License.
Full license can be found in the "LICENSE" file in the repository root directory.

Copyright (c) 2024 Matt Young

Contains functions that apply convolutions such as the sample mean to generated datasets.
"""

""" Calculates the estimated mean values at each possible sampling window start position.

Args:
    dataset(list[int]): 0s and 1s that comprise the dataset that represents the raw key
    window_size(int): the size of the sampling window to use to obtain the sample means

Returns:
    A list of floating point values in the range 0 to 1 giving the sample means at each point in the dataset.
    The size of this list is len(dataset)-window_size
"""
def est_mean(dataset, window_size):
    est_mean_vals = []

    # For each possible sampling window starting position...
    # (Note that the positions used on the x-axes of the plots in the paper are the END positions of the sampling window)
    current_pos = 0
    while(current_pos < len(dataset) - window_size):
        # Calculate the estimated mean for the current sampling window position
        est_mean = sample_mean(dataset, current_pos, window_size)
        est_mean_vals.append(est_mean)

        # Increments the current sampling window position
        current_pos += 1

    return est_mean_vals

""" Calculates the sample mean of the values in the dataset within the range specified.

Args:
    dataset(list[int]): 0s and 1s that comprise the dataset that represents the raw key
    sample_start(int): position in the dataset to start sampling from
    sample_size(int): the size of the sample to take the mean over

Returns:
    A floating point value that is the sample mean of the dataset over the specified range

Raises:
    ValueError: Dataset is empty, or the specified sampling start and/or end positions are outside the size of the dataset and/or less than 0
"""
def sample_mean(dataset: list[int], sample_start: int, sample_size: int):
    # Input validation
    if(len(dataset) == 0
       or sample_start < 0
       or sample_start > len(dataset)-1
       or sample_size < 0
       or (sample_start + sample_size) > len(dataset)):
        raise ValueError('Parameters to sample_mean function incorrect!')
    
    # Uses list slicing to get the required sample from the dataset
    samples = dataset[sample_start:sample_start+sample_size]
    # Calculates and returns the mean of the sample
    return sum(samples)/len(samples)
        