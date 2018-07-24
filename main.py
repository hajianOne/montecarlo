#!/usr/bin/env python3

from random import uniform
from sampling.montecarlo import MonteCarlo

def sampling_func():
    x = uniform(0.0, 1.0)   
    y = uniform(0.0, 1.0)

    if (x**2 + y**2 <= 1):
        return (x, y, True)
    else:
        return (x, y, False)

def aggregate_func(samples):

    count_true  = 0
    count_total = len(samples)

    for sample in samples:
        _, _, status = sample
        if status == True:
            count_true += 1

    return {
        "pi": (4.0 * count_true / count_total),
        "true": [(x,y) for (x,y,status) in samples if status==True],
        "false": [(x,y) for (x,y,status) in samples if status==False]
        }



def simulate():
    num_samples = 10000
    n_jobs = 2

    mc = MonteCarlo(sampling_func, aggregate_func)
    result = mc.simulate(num_samples, n_jobs)
    return result

# print ("pi: {}".format(pi))

if __name__=="__main__":
    import matplotlib.pyplot as plt
    result = simulate()

    true = {"x": [x for (x,y) in result["true"]], 
            "y": [y for (x,y) in result["true"]], 
    }

    false = {"x": [x for (x,y) in result["false"]], 
             "y": [y for (x,y) in result["false"]], 
    }
    plt.plot(true["x"], true["y"], "o")
    plt.plot(false["x"], false["y"], "o")
    plt.title("Pi ~ {}".format(result["pi"]))
    plt.show()

