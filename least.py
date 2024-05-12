import numpy as np
# importing the library
from memory_profiler import profile
from env import TESTING
from tp_potential import Data


def least_cost_cell_method(data: Data, method: str):
    cost_matrix = data.c
    supply = data.a
    demand = data.b
    num_sources = len(supply)
    num_destinations = len(demand)

    # Initialize the transportation matrix
    transport_matrix = np.zeros((num_sources, num_destinations))

    # Create a copy of the cost matrix for tracking remaining cells
    remaining_matrix = cost_matrix.copy()

    # Define a large finite value to represent allocated cells
    ALLOCATED = 1e5

    # Iterate until all supplies and demands are exhausted
    while np.sum(supply) > 0 and np.sum(demand) > 0:
        # Find the cell with the minimum cost
        min_cost = np.min(remaining_matrix)
        min_cost_indices = np.argwhere(remaining_matrix == min_cost)

        # Select the first occurrence of the minimum cost cell
        i, j = min_cost_indices[0]

        # Determine the allocation for the selected cell
        allocation = min(supply[i], demand[j])
        transport_matrix[i, j] = allocation

        # Update the remaining supply and demand
        supply[i] -= allocation
        demand[j] -= allocation

        # Mark the cell as allocated by setting its cost to the large finite value
        remaining_matrix[i, j] = ALLOCATED

        # If the supply at the current source is exhausted, mark the corresponding row as allocated
        if supply[i] == 0:
            remaining_matrix[i, :] = ALLOCATED

        # If the demand at the current destination is satisfied, mark the corresponding column as allocated
        if demand[j] == 0:
            remaining_matrix[:, j] = ALLOCATED

    # Calculate the total transportation cost
    total_cost = np.sum(cost_matrix * transport_matrix)

    return transport_matrix, total_cost


if TESTING:
    least_cost_cell_method = profile(least_cost_cell_method)

# # Define the cost matrix, supply, and demand
# cost_matrix = np.array([[10, 2, 20, 11], 
#                         [12, 7, 9, 20],
#                         [4, 14, 16, 18]])
# supply = np.array([15, 25, 10])
# demand = np.array([5, 15, 15, 15])

# # Solve the transportation problem using the Least Cost Cell Method
# transport_matrix, total_cost = least_cost_cell_method(cost_matrix, supply, demand)

# # Print the solution
# print("Solution using Least Cost Cell Method:")
# print("Total transportation cost:", total_cost)
# print("Transportation matrix:")
# print(transport_matrix)
