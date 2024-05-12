import numpy as np
import random

def round_to(x: float, n: int):
    return int(x * pow(10, n)) / pow(10, n)

def generate_random_transport_problem(num_sources, num_destinations, min_cost, max_cost, min_supply, max_supply, min_demand, max_demand):
    # Generate random cost matrix
    cost_matrix = np.random.randint(min_cost, max_cost + 1, size=(num_sources, num_destinations))

    # Generate random supply values
    supply = np.random.randint(min_supply, max_supply + 1, size=num_sources)
    
    # Generate random demand values
    demand = np.random.randint(min_demand, max_demand + 1, size=num_destinations)
    
    # Adjust demand values to match total supply
    total_supply = np.sum(supply)
    total_demand = np.sum(demand)
    if total_supply > total_demand:
        # Increase demand values proportionally
        demand = (demand * total_supply / total_demand).astype(int)
    elif total_supply < total_demand:
        # Decrease demand values proportionally
        demand = (demand * total_supply / total_demand).astype(int)
    difference = np.sum(supply) - np.sum(demand)
    supply[0] -= difference
    
    return cost_matrix, supply, demand

# importing the module
import tracemalloc
import time
import copy

def test_time_mem(func, cost_matrix, supply=np.array(0), demand=np.array(0), potential=False, data=None):
    start_time = time.time()
    # starting the monitoring
    tracemalloc.start()
    
    transportation_matrix = None
    cost = None
    if not potential:
        transportation_matrix, cost = func(copy.deepcopy(cost_matrix), supply.copy(), demand.copy())
    else:
        transportation_matrix, cost = func(data)
    # displaying the memory
    mem = tracemalloc.get_traced_memory()
    # print(f"Memory trace: {mem}")
 
    # stopping the library
    tracemalloc.stop()
    
    end_time = time.time()
    execution_time = int((end_time - start_time) * 10000) / 10000
    # print(f"Execution time: {execution_time} seconds")
    
    return dict(transportation_matrix = transportation_matrix, cost = cost, time = execution_time, memory = (mem[1] - mem[0]))

from threading import Thread
import functools

def timeout(timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, timeout))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(timeout)
            except Exception as je:
                print ('error starting thread')
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco