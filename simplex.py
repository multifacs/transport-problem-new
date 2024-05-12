import numpy as np
from scipy.optimize import linprog

# importing the library
from memory_profiler import profile
from env import TESTING

def simplex_method(cost_matrix, supply, demand, method="simplex"):
    # Create the coefficient matrix for the constraints
    num_sources = len(supply)
    num_destinations = len(demand)
    num_variables = num_sources * num_destinations

    A_eq = np.zeros((num_sources + num_destinations, num_variables))

    # Supply constraints
    for i in range(num_sources):
        start = i * num_destinations
        end = (i + 1) * num_destinations
        A_eq[i, start:end] = 1

    # Demand constraints
    for j in range(num_destinations):
        for i in range(num_sources):
            A_eq[num_sources + j, i * num_destinations + j] = 1

    # Flatten the cost matrix
    c = cost_matrix.flatten()

    # Set up the equality constraints
    b_eq = np.concatenate((supply, demand))

    # Solve the linear programming problem
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, method=method)

    return res.x.reshape((num_sources, num_destinations)), res.fun

if TESTING:
    simplex_method = profile(simplex_method)

# # Define the cost matrix
# cost_matrix = np.array([[10, 2, 20, 11], 
#                         [12, 7, 9, 20],
#                         [4, 14, 16, 18]])

# # Define the supply and demand constraints
# supply = np.array([15, 25, 10])
# demand = np.array([5, 15, 15, 15])

# transport_matrix, total_cost = simplex_method(cost_matrix, supply, demand)

# # Print the optimal solution
# print("Optimal solution:")
# print("Total transportation cost:", total_cost)

# print("Transportation matrix:")
# print(transport_matrix)