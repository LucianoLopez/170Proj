import sys
import random
import networkx as nx


def generate_buses(buses, bus_capacity, students):
	list_of_buses = []
	list_of_students = random.sample(range(students), students)
	start, max = 0, bus_capacity

	for bus in range(buses):
		list_of_buses.append(list_of_students[start:max])
		start = max
		max += bus_capacity

	return list_of_buses

def generate_graph(bus_list, probability, students):
	g = nx.Graph()
	g.add_nodes_from([x for x in range(students)])
	for bus in range(len(bus_list)):
		for i in range(len(bus_list[bus])):
			percentage = random.choice(probability)
			amt_of_friends = int(percentage * len(bus_list[bus]))
			amt_of_friends_out = int(1-percentage * len(bus_list[bus]))
			lst = bus_list[bus][:i] + bus_list[bus][i+1:len(bus_list[bus])]
			bus_options = [x for x in range(len(bus_list)) if x != bus]
			options = random.sample(range(len(bus_list[bus])), amt_of_friends)
			friends = [bus_list[bus][x] for x in options]
			for _ in range(amt_of_friends_out):
				select_bus = random.choice(bus_options)
				select_friend = random.choice(range(len(bus_list[bus])))
				friends.append(bus_list[select_bus][select_friend])
			# g.add_edges_from(friends)
			for friend in friends:
				g.add_edge(bus_list[bus][i], friend)
	return g

def generate_constraints(bus_list, size):
	constraints = []

	for _ in range(size):
		# print(len(bus_list))
		bus = random.sample(range(len(bus_list)), 2)
		print(bus)
		length = len(bus_list[bus[0]])
		print(len(bus_list[bus[0]]))
		# print(bus_list)
		constraint_len = random.choice(range(2, length))
		print(constraint_len)
		amt_in_bus = random.choice(range(1, constraint_len + 1))

		# print(len(bus_list[0]))
		# print(amt_in_bus)
		samples = random.sample(range(len(bus_list[bus[0]])), amt_in_bus)
		constraint = [bus_list[bus[0]][x] for x in samples]
		## CAN MAKE BETTER
		outside = [bus_list[bus[1]][x] for x in random.sample(range(1, len(bus_list[bus[1]])), constraint_len - amt_in_bus)]
		# outside = random.sample(bus_list[bus[1]], constraint_len - amt_in_bus)
		constraint += outside
		constraints.append(constraint)

	return constraints

def generate_files(list_of_buses, graph, constraints):
	file = open('./inputs/'+size_name+'/parameters.txt', "w")
	file.write("%d\n" %len(list_of_buses))
	file.write("%d\n" %len(list_of_buses[0]))
	for constraint in constraints:
		file.write(str(constraint) + "\n")
	file.close()
	nx.write_gml(graph, './inputs/'+size_name+'/graph.gml')
	file = open('./outputs/'+size_name+'.out', "w")
	for bus in list_of_buses:
		file.write(str(bus) + "\n")
	file.close()


##Driver Function

def generate(students, bus_amount, bus_capacity, rowdy_list_size):
	list_of_buses = generate_buses(bus_amount, bus_capacity, students)
	g = generate_graph(list_of_buses, [.75, .8, .9], students)
	constraints = generate_constraints(list_of_buses, rowdy_list_size)
	generate_files(list_of_buses, g, constraints)

size_name = "small"
generate(25, 5, 5, 5)
size_name = "medium"
generate(400, 10, 40, 50)
size_name = "large"
generate(800, 25, 32, 120)











