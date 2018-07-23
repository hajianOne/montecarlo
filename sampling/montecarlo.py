#!/usr/bin/env python3
import multiprocessing

class MonteCarlo_Sampler(object):

    def __init__(self, sampling_func, aggregate_func):
        self.sampling_func = sampling_func
        self.aggregate_func = aggregate_func

        self.samples = []
        
    def simulate(self, num_samples):
        '''
        take samples from sampling_func

        num_samples: int
        '''
        for i in range(num_samples):
            self.samples.append(self.sampling_func())
    
class MonteCarlo(object):

    def __init__(self, sampling_func, aggregate_func):
        """MonteCarlo class implements a MonteCarlo method with parallel
        capabilites.

        sampling_func: a pointer to a python function 

        aggregate_func: a pointer to a python function
        """

        self.sampling_func = sampling_func
        self.aggregate_func = aggregate_func

        self.samples = []

    def sampler_simulate(self, num_samples_sampler):

        mc_s = MonteCarlo_Sampler(self.sampling_func,
                                  self.aggregate_func)

        mc_s.simulate(num_samples_sampler)

        return mc_s.samples
        
    def simulate(self, num_samples, n_jobs):
        '''
        simulate monte carlo in parallel.

        num_samples: int

        n_jobs: int
        number of cpu threads to use.
        '''

        self.num_samples = num_samples
        self.n_jobs = n_jobs

        self.num_samples_sampler = self.num_samples // n_jobs

        self.params = [self.num_samples_sampler] * n_jobs
        
        pool = multiprocessing.Pool(self.n_jobs)

        samplers_result = pool.map_async(self.sampler_simulate,
                                         self.params)
                
        self.results = samplers_result.get()

        pool.close()
        pool.join()

        for result in self.results:
            self.samples += result

        return self.aggregate_func(self.samples)



if __name__=="__main__":

    from random import uniform
    
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


    
    num_samples = 10000000
    n_jobs = 4

    mc = MonteCarlo(sampling_func, aggregate_func)
    pi = mc.simulate(num_samples, n_jobs)

    print ("pi: {}".format(pi))
