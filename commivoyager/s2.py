
import math
from collections import namedtuple
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def create_distance_matrix(points, nodeCount):
    mtr = []
    for i in range(0, nodeCount):
        row = []
        for j in range(0, nodeCount):
            row.append((int)(length(points[i], points[j]) * 100))
        mtr.append(row)
    return mtr

def print_solution(manager, routing, solution):
        """Prints solution on console."""
        print('Objective: {} miles'.format(solution.ObjectiveValue()))
        index = routing.Start(0)
        plan_output = 'Route for vehicle 0:\n'
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} ->'.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output += ' {}\n'.format(manager.IndexToNode(index))
        #print(plan_output)
        plan_output += 'Route distance: {}miles\n'.format(route_distance)

def get_routes(solution, routing, manager):
    routes = []
    for route_nbr in range(routing.vehicles()):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))


    mtr = create_distance_matrix(points, nodeCount)
    num_vehicles = 1
    depot = 0

    manager = pywrapcp.RoutingIndexManager(nodeCount, num_vehicles, depot)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return mtr[from_node][to_node]#length(from_node, to_node)

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    sol = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    #if solution:
      #  print_solution(solution, routing, manager)
    if sol:
        #print_solution(manager, routing, sol)
        print_sol = get_routes(sol, routing, manager)
        # print(print_sol)
    solution = print_sol[0]
    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount):
        obj += length(points[solution[index]], points[solution[index+1]])


    # obj /= 100
    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += '\n'.join(map(str, solution))

    return output_data

#5
import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        with open("output.txt", "w") as text_file:
            text_file.write(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')



