import networkx as nx
import os

from gurobipy import *

###########################################
# Change this variable to the path to 
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./all_inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a 
# different folder
###########################################
path_to_outputs = "./outputs"

def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(folder_name + "/graph.gml")
    parameters = open(folder_name + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []
    
    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)

    return graph, num_buses, size_bus, constraints


def create_variables(graph):

	variableEdgeAmt = {}
	variables = list(graph.nodes)

	for variable in variables:
		variableEdgeAmt[variable] = list(graph.adj[variable])

	# print(variableEdgeAmt)
	return variableEdgeAmt

def create_model(graph, buses, bus_size, constraints, variablesAdjDic):
	indicator_variables = {}
	m = Model("")
	m.Params.TIME_LIMIT = 600.0
	##Creates the indicator variable for the model
	for i in variablesAdjDic:
		for bus in range(buses):
			indicator_variables[(i, bus)] = m.addVar(vtype=GRB.BINARY)
	# ##Creates the integer variables
	# for i in variablesAdjDic:
	# 	integer_variables[i] = m.addVar(vtype=GRB.INTEGER, name=i)

	##Create optimization func TODO
	# print(indicator_variables)

	m.setObjective(quicksum(indicator_variables[(variable, bus)] * sum(indicator_variables[(i, bus)] for i in variablesAdjDic[variable])/float(len(variablesAdjDic[variable])) if len(variablesAdjDic[variable]) >= 1 else indicator_variables[(variable, bus)]
							for variable, bus in indicator_variables), GRB.MAXIMIZE)

	##Create the constraints

	num = 0
	for constraint in constraints:
		num +=1
		for bus in range(buses):
			lst = []
			for variable in constraint:
				lst.append(indicator_variables[(variable, bus)])
			m.addConstr(quicksum(lst[i] for i in range(len(lst))) <= len(constraint) - 1) #TODO: ADD ACTUAL CONSTRAINTS

	##enforces that for all variables, they are only present in one bus
	num = 0
	for variable in variablesAdjDic:
		num +=1
		lst = []
		for bus in range(buses):
			lst.append(indicator_variables[(variable,bus)])
		m.addConstr(quicksum(lst[i] for i in range(len(lst))) == 1)

	for bus in range(buses):
		lst = []
		for variable in variablesAdjDic:
			lst.append(indicator_variables[(variable, bus)])
		m.addConstr(quicksum(lst[i] for i in range(len(lst))) <= bus_size)



	return m, indicator_variables




# def fix_collision(constraints, numFriendsDic, busDictionary):
#
# 	for constraint in constraints:
# 		enforced = False
# 		curBus = busDictionary[constraints[0]]
# 		for person in constraint:
# 			if busDictionary[person] is not curBus:
# 				enforced = True
# 				break
# 		if not enforced:



def solve(graph, num_buses, size_bus, constraints):
	#TODO: Write this method as you like. We'd recommend changing the arguments here as well

	variablesAdjDic = create_variables(graph)
	model, indicator_variables = create_model(graph, num_buses, size_bus, constraints, variablesAdjDic)
	model.optimize()
	solution = []
	for bus in range(num_buses):
		solution.append([])
	# print(indicator_variables)
	# for v in model.getVars():
	# 	print(v.varName, v.x)
	if model.status == GRB.Status.OPTIMAL:
		for variable_key, variable_item in indicator_variables.items():
			if variable_item.x == 1.0:
				solution[variable_key[1]].append(variable_key[0])
	return solution


def main():
	'''
		Main method which iterates over all inputs and calls `solve` on each.
		The student should modify `solve` to return their solution and modify
		the portion which writes it to a file to make sure their output is
		formatted correctly.
	'''
	size_categories = ["small", "medium", "large"]
	if not os.path.isdir(path_to_outputs):
		os.mkdir(path_to_outputs)

	for size in size_categories:
		category_path = path_to_inputs + "/" + size
		output_category_path = path_to_outputs + "/" + size
		category_dir = os.fsencode(category_path)

		if not os.path.isdir(output_category_path):
			os.mkdir(output_category_path)

		for input_folder in os.listdir(category_dir):
			input_name = os.fsdecode(input_folder)
			if input_name == ".DS_Store":
				continue
			graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
			solution = solve(graph, num_buses, size_bus, constraints)
			output_file = open(output_category_path + "/" + input_name + ".out", "w")
			#TODO: modify this to write your solution to your
			#      file properly as it might not be correct to
			#      just write the variable solution to a file
			for bus in solution:
				output_file.write(str(bus)+ "\n")

			output_file.close()

if __name__ == '__main__':
	main()


