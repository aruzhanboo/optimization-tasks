import sys
import pandas as pd

from ortools.sat.python import cp_model

def parse_input(input_data):
    lines = input_data.split("\n")
    first_line = lines[0].split()
    num_nodes = int(first_line[0])
    edge_count = int(first_line[1])
    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
    return num_nodes, edges

def graph_coloring(num_nodes, connections, k, timeout=None):
    model = cp_model.CpModel()
    nodes = [model.NewIntVar(0, k - 1, f"x{i}") for i in range(num_nodes)]

    for i, conn in enumerate(connections):
        if i == 0:
            model.Add(nodes[conn[0]] == 0)
            model.Add(nodes[conn[1]] == 1)
        else:
            model.Add(nodes[conn[0]] != nodes[conn[1]])
    solver = cp_model.CpSolver()
    if timeout:
        solver.parameters.max_time_in_seconds = timeout
    status = solver.Solve(model)
    if status != cp_model.OPTIMAL:
        return None
    colors = [solver.Value(node) for node in nodes]
    return colors

def print_output(num_nodes, solution):
    df = pd.DataFrame(solution)
    output_data = str(num_nodes) + " " + str(0) + "\n"
    output_data += " ".join(map(str, solution))
    df.to_excel(r'C:\Users\User\Desktop\optim\task1\soluton1.xlsx', index = False, header = False)
    return output_data

def find_minimum_colors(num_nodes, edges):
    k = num_nodes
    solution = graph_coloring(num_nodes, edges, k)
    timeout = 120
    while solution:
        print(k)
        upper_bound_solution = solution
        k = len(set(solution)) // 2
        solution = graph_coloring(num_nodes, edges, k, timeout)

    upper_bound = k * 2
    lower_bound = k
    while abs(upper_bound - lower_bound) > 1:
        k = (lower_bound + upper_bound + 1) // 2
        print(k, lower_bound, upper_bound)
        if k == upper_bound:
            break
        solution = graph_coloring(num_nodes, edges, k, timeout)
        if solution:
            upper_bound = k
            upper_bound_solution = solution
        else:
            lower_bound = k
    return upper_bound_solution, len(set(upper_bound_solution))

def solve_it(input_data):
    num_nodes, edges = parse_input(input_data)
    solution, k = find_minimum_colors(num_nodes, edges)
    output_data = print_output(k, solution)
    return output_data

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, "r") as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            "This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)"
        )