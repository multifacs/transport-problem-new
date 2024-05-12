import numpy as np
# importing the library
from memory_profiler import profile
from env import TESTING

def northwest_corner_method(cost_matrix, supply, demand):
    num_sources = len(supply)
    num_destinations = len(demand)
    
    # Initialize the transportation matrix
    transport_matrix = np.zeros((num_sources, num_destinations))
    
    # Iterate over the sources and destinations
    i = 0
    j = 0
    while i < num_sources and j < num_destinations:
        if supply[i] < demand[j]:
            transport_matrix[i, j] = supply[i]
            demand[j] -= supply[i]
            i += 1
        elif supply[i] > demand[j]:
            transport_matrix[i, j] = demand[j]
            supply[i] -= demand[j]
            j += 1
        else:
            transport_matrix[i, j] = supply[i]
            i += 1
            j += 1
    
    # Calculate the total transportation cost
    total_cost = np.sum(cost_matrix * transport_matrix)
    
    return transport_matrix, total_cost

if TESTING:
    northwest_corner_method = profile(northwest_corner_method)

# # Define the cost matrix, supply, and demand
# cost_matrix = np.array([[10, 2, 20, 11], 
#                         [12, 7, 9, 20],
#                         [4, 14, 16, 18]])
# supply = np.array([15, 25, 10])
# demand = np.array([5, 15, 15, 15])

# # Solve the transportation problem using the Northwest Corner Method
# transport_matrix, total_cost = northwest_corner_method(cost_matrix, supply, demand)

# # Print the solution
# print("Solution using Northwest Corner Method:")
# print("Total transportation cost:", total_cost)
# print("Transportation matrix:")
# print(transport_matrix)