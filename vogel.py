import numpy as np
# importing the library
from memory_profiler import profile
from env import TESTING

from misc import timeout

# @profile
@timeout(1)
def vogels_approximation_method(cost_matrix, supply, demand):
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
        # Calculate the penalty for each row and column
        row_penalties = np.zeros(num_sources)
        col_penalties = np.zeros(num_destinations)
        
        for i in range(num_sources):
            if supply[i] > 0:
                remaining_row = remaining_matrix[i, :]
                sorted_row = np.sort(remaining_row[remaining_row != ALLOCATED])
                if len(sorted_row) > 1:
                    row_penalties[i] = sorted_row[1] - sorted_row[0]
                else:
                    row_penalties[i] = sorted_row[0]
        
        for j in range(num_destinations):
            if demand[j] > 0:
                remaining_col = remaining_matrix[:, j]
                sorted_col = np.sort(remaining_col[remaining_col != ALLOCATED])
                if len(sorted_col) > 1:
                    col_penalties[j] = sorted_col[1] - sorted_col[0]
                else:
                    col_penalties[j] = sorted_col[0]
        
        # Find the row or column with the maximum penalty
        max_penalty = max(np.max(row_penalties), np.max(col_penalties))
        
        if max_penalty in row_penalties:
            i = np.argmax(row_penalties)
            j = np.argmin(remaining_matrix[i, :])
        else:
            j = np.argmax(col_penalties)
            i = np.argmin(remaining_matrix[:, j])
        
        # Determine the allocation for the selected cell
        allocation = min(supply[i], demand[j])
        transport_matrix[i, j] = allocation
        
        # Update the remaining supply and demand
        supply[i] -= allocation
        demand[j] -= allocation
        
        # Mark the cell as allocated by setting its cost to infinity
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


# # Define the cost matrix, supply, and demand
# cost_matrix = np.array([[10, 2, 20, 11], 
#                         [12, 7, 9, 20],
#                         [4, 14, 16, 18]])
# supply = np.array([15, 25, 10])
# demand = np.array([5, 15, 15, 15])

# # Solve the transportation problem using Vogel's Approximation Method
# transport_matrix, total_cost = vogels_approximation_method(cost_matrix, supply, demand)

# # Print the solution
# print("Solution using Vogel's Approximation Method:")
# print("Total transportation cost:", total_cost)
# print("Transportation matrix:")
# print(transport_matrix)