#!/usr/bin/env python3

import pytest

from sampling.montecarlo import MonteCarlo
from sampling.montecarlo import MonteCarlo_Sampler

from random import uniform

def instantiate_sampler():
    def sampling_func():
        return True
    def aggregate_func():
        return False
    return MonteCarlo_Sampler(sampling_func, aggregate_func) 

def test_instantiate_sampler():
    mc_s = instantiate_sampler()

    errors = []

    if mc_s.sampling_func() != True:
        errors.append(True)
    if mc_s.aggregate_func() != False:
        errors.append(True) 
    if not isinstance(mc_s.samples, list):
        errors.append(True)
        
    assert not errors

def test_simulate_sampler():
    mc_s = instantiate_sampler()

    errors = []
    n = 1000
    mc_s.simulate(n)

    if len(mc_s.samples) != n:
        errors.append(True)
    for i in mc_s.samples:
        if i != True:
            errors.append(True)

    assert not errors
    
def instantiate():
    return MonteCarlo(lambda x: x, lambda y: -y) 
    
def test_instantiate():
    mc = instantiate()

    errors = []

    if mc.sampling_func(1) != 1:
        errors.append(True)
    if mc.aggregate_func(1) != -1:
        errors.append(True) 

    assert not errors

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

def test_simulate():

    mc = MonteCarlo(sampling_func, aggregate_func)

    num_samples = 1000000
    n_jobs = 4

    pi = mc.simulate(num_samples, n_jobs)

    errors = []

    if mc.n_jobs != n_jobs:
        errors.append("n_jobs")

    if mc.num_samples_sampler != num_samples // n_jobs:
        errors.append("num_samples_sampler")
    if len(mc.params) != n_jobs:
        errors.append("params")
    if len(mc.results) != n_jobs:
        errors.append("results")
    if len(mc.samples) != num_samples:
        errors.append("size of the sample")

    assert not errors
    
