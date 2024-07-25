from sim.datasetGenerator import *
from sim.distributions import *
from sim.tests import *
from sim.utils import *
from sim.convolutions import *

import matplotlib.pyplot as plt

import numpy as np

import time

# params[0] - num samples
# params[1] - num trials
def calculate_trials_results(params):
    print(params[0])
    prob_dist_pattern = [
    # (const_0, 5), 
    # (const_1, 5), 
    (uniform_dist, int(params[0])),
    (lower_third, int(params[0]))
    ]
    trials_results_list = []
    for t in range(params[1]):
        dataset = generate_dataset(prob_dist_pattern);
        est_means_list = est_mean(dataset[1], int(params[0]))

        for i in range(len(est_means_list)):
            if abs(0.5-est_means_list[i])>=0.05:
                trials_results_list.append(i)
                break
    return (params[0], trials_results_list)

if __name__ == '__main__':

    start_time = time.time()

    def std_dev(population):
        n = len(population)
        mu = sum(population)/n
        s = math.sqrt(sum([((x-mu)**2) for x in population])/n)
        return s

    def lin_reg(x_inp, y_inp):
        x = np.array([[1, a] for a in x_inp])
        y = np.array(y_inp)
        beta = np.matmul(np.transpose(x), x)
        beta = np.linalg.inv(beta)
        beta = np.matmul(beta, np.transpose(x))
        beta = np.matmul(beta, y)
        return beta

    def rmse(lin_reg_coeff, x, y):
        error = math.sqrt(sum([(y - (lin_reg_coeff[0] + (x * lin_reg_coeff[1])))**2 for x, y in zip(x, y)])/len(y))
        return error

    plot_results = True

    # Datapoints from Fig.### of the paper
    # num_samples = np.linspace(100, 50000, 16)
    # n_trials = 1000

    # Smaller example
    num_samples = np.linspace(10, 1000, 4)
    num_samples = [int(x) for x in num_samples]
    n_trials = 100
    
    block_size = 10
    num_blocks = int(n_trials/block_size)

    block_num_samples = []
    for n in num_samples:
        block_num_samples = block_num_samples + ([int(n)] * num_blocks)

    block_sizes = [block_size] * len(block_num_samples)

    # Multi threading time
    # Fingers Crossed

    import multiprocessing

    try:
        cpus = multiprocessing.cpu_count()
    except NotImplementedError:
        cpus = 2

    pool = multiprocessing.Pool(processes=cpus)
    results_list = pool.map(calculate_trials_results, zip(block_num_samples, block_sizes))

    # End of multi threading time

    res_dict = {}

    for res in results_list:
        if res[0] not in res_dict:
            res_dict.update({res[0] : res[1]})
        else:
            res_dict.update({res[0] : res_dict.get(res[0]) + res[1]})

    res_list = []
    for x in res_dict:
        res_list.append(res_dict.get(x))

    trial_means = [sum(trial)/len(trial) for trial in res_list]
    std_devs = [std_dev(trial) for trial in res_list]

    coefficients = lin_reg(num_samples, trial_means)
    print(coefficients)

    error = rmse(coefficients, num_samples, trial_means)

    if plot_results:
        plt.subplot(2, 1, 1)
        plt.grid()
        plt.scatter(num_samples, trial_means, marker='x', color='red')
        plt.plot([num_samples[0], num_samples[len(num_samples)-1]], 
                [coefficients[0] + (coefficients[1] * num_samples[0]), coefficients[0] + (coefficients[1] * (num_samples[len(num_samples)-1]))],
                linestyle='dashed')

        plt.subplot(2, 1, 2)
        plt.grid()
        plt.plot(num_samples, std_devs, marker='x')

        plt.show()
    else:

        f = open("foo.txt", "w")
        f.write(str(coefficients) + "\n")
        f.write("RMSE: " + str(error) + "\n")
        f.write("--- %s seconds ---\n" % (time.time() - start_time))
        f.write(str(num_samples) + "\n") 
        f.write(str(trial_means) + "\n")
        f.write(str(std_devs))
        f.close()

