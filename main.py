#!/usr/bin/env python3

from random import uniform
from sampling.montecarlo import MonteCarlo

def sampling_func():
    x = uniform(0.0, 1.0)   
    y = uniform(0.0, 1.0)

    if (x**2 + y**2 <= 1):
        return True
    else:
        return False

def aggregate_func(samples):

    count_true  = 0
    count_total = len(samples)

    for sample in samples:
        if sample == True:
            count_true += 1

    return (4.0 * count_true / count_total)



num_samples = 20000000
n_jobs = 2

mc = MonteCarlo(sampling_func, aggregate_func)
pi = mc.simulate(num_samples, n_jobs)

print ("pi: {}".format(pi))
