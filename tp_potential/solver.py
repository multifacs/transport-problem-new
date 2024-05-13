from typing import Any, List

import numpy as np
# importing the library
from memory_profiler import profile
from env import TESTING

from misc import timeout

from .Data import Data
from .plan import (find_cycle_path, get_start_plan_by_min_element_method,
                   get_start_plan_by_north_west_corner_method,
                   is_degenerate_plan, make_start_plan_non_degenerate,
                   recalculate_plan)

MAX_ITER = 100


# @profile
@timeout(2)
def solve(data: Data, method: str, use_nw_corner_method: bool = False):
    try:
        if use_nw_corner_method:
            x = get_start_plan_by_north_west_corner_method(data)
        else:
            x = get_start_plan_by_min_element_method(data)
        # x = data.c
        # print(x)

        check_res = is_degenerate_plan(x)
        if check_res:
            make_start_plan_non_degenerate(x)

        iter = 0
        while iter < MAX_ITER:
            iter += 1
            cost = data.calculate_cost(x)
            p = data.calculate_potentials(x)
            check_res = data.is_plan_optimal(x, p)
            if check_res:
                break

            cycle_path = find_cycle_path(x, data.get_best_free_cell(x, p))
            o = recalculate_plan(x, cycle_path)

        # print(f"Iterations: {iter}")
        # print(x)
        # print(data.calculate_cost(x))
    except Exception as e:
        print(e)

    return x, data.calculate_cost(x)

# if TESTING:
#     solve = profile(solve)
