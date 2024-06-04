from sim.tests import *

# TODO Could replace this with a list comprehension and move sample_mean here, as 'convolutions' better describes that function
def est_mean(dataset, num_samples):
    est_mean_vals = []

    # Calculates the estimated mean values for 
    current_pos = 0
    while(current_pos < len(dataset) - num_samples):

        # if(current_pos % 1000 == 0):
        #     print(current_pos)

        est_mean = sample_mean(dataset, current_pos, num_samples)
        est_mean_vals.append(est_mean)

        current_pos += 1
    
    return est_mean_vals

def est_mean_threshold(dataset, num_samples, nominal, threshold):
    est_mean_vals = []

    # Calculates the estimated mean values for 
    current_pos = 0
    while(current_pos < len(dataset) - num_samples):

        # if(current_pos % 1000 == 0):
        #     print(current_pos)

        est_mean = sample_mean(dataset, current_pos, num_samples)
        est_mean_vals.append(est_mean)
        
        if((est_mean < nominal-threshold) or (est_mean > nominal+threshold)):
            return current_pos

        current_pos += 1
    
    return current_pos