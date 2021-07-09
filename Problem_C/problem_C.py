# Daniel Torres
import sys
from copy import deepcopy


# Description: It transforms all the data in the current unit to all other units of which 
# we have an equivalent rule.
# Receives: A dictionary=final_path to store some new equivalencies, a dictionary=unit_paths.
# with the initial unit transformations, the current unit=key which we are trying to get all
# possible transformations, the unit=current_unit which is the current unit of the original data and
# the units=values which we can transform the data into.
# Returns: A dictionary with all possible unit transformations.
def travel_path(final_path, unit_paths, key, current_unit, values):
    if len(values):
        for unit, ratio in values.items():
            if unit not in final_path[key] and unit != key:
                final_path[key][unit] = final_path[key][current_unit]*ratio
                next_nodes = unit_paths[unit]
                final_path = travel_path(final_path, unit_paths, key, unit, next_nodes)
    return final_path


# Description: Starting from the original equivalencies the functions performs every
# possible unit transformation and return them so the transitions can be bidirectional.
# Receives: An empty dictionary which will indicate all possible paths to
#       take between units and a units paths with the original equivalencies.
# Returns: The dictionary with all the possible equivalencies between the units.
def find_paths_between_units(final_path, unit_paths):
    for key, values in unit_paths.items():
        if len(values):
            for unit, ratio in values.items():
                next_values = unit_paths[unit]
                final_path = travel_path(final_path, unit_paths, key, unit, next_values)
    return final_path


# Description: The functions transforms the answer stored in the dictionary which
# contains one path that traverses every unit to the required format for the output.
# Receives: A dictionary with a key for every unit and a unic value to transform to.
# Returns: A string=s with the conversion factors defined with respect to the leftmost unit.
def build_equivalent_conversions(solution):
    index = 1
    acc = 1
    s = ''
    while (True):
        try:
            acc *= solution[index][0]
            s += str(acc) + solution[index][1] + ' = '
            index = solution[index][1]
        except KeyError:
            return s
                

# Description: The function picks the closest relations between units to
# establish an ordered chain of equivalencies.
# Receives: A dictionary with all the possible transformations between two units.
# Returns: A dictionary=solution with a key for every unit and a unic value to transform to.
def order_units(final_path):
    solution = {}
    for key, value in final_path.items():
        biggest_of_smallest_differences = None
        name = None
        for k, v in value.items():
            if v < 1.0:
                if biggest_of_smallest_differences == None or biggest_of_smallest_differences < v:
                    biggest_of_smallest_differences = v
                    name = k
        if biggest_of_smallest_differences != None:
            solution[name] = (int(1/biggest_of_smallest_differences), key)
        else:
            solution[1] = (1, key)
    return solution


while (True):
    N = int(sys.stdin.readline().rstrip())
    if not N:
        exit(0)

    units = sys.stdin.readline().split()
    # This dictionary will be used to trace all possible equivalences between units.
    unit_paths = {x:{} for x in units}
    
    for row in range(N-1):
        line = sys.stdin.readline().split('=')
        start = line[0][:-1]
        rate, end = line[1].split()
        unit_paths[start][end] = int(rate)
        unit_paths[end][start] = 1/int(rate)
    final_path = deepcopy(unit_paths)
    
    final_path = find_paths_between_units(final_path, unit_paths)

    solution = order_units(final_path)
    
    s = build_equivalent_conversions(solution)
    print(s[:-3])
