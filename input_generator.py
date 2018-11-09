import sys
import random
import networkx as nx
import matplotlib.pyplot as plt
#Default size
size = 10
size_name = "small"
length = 15
"""
###################################################
#RECEIVES INPUT OF FORM: GRAPH_SIZE ROWDYLIST_SIZE#
###################################################
"""

"""Sanitize Inputs"""
if len(sys.argv) > 3:
	print("Invalid Input... Input should be an integer")
	exit()

try:
	size = int(sys.argv[1])
	length = int(sys.argv[2])
	if size > 500:
		size_name = "large"
		assert length < 2000, "Rowdy List for size " + size_name + " must not be greater than 2000"
	elif size > 250:
		size_name = "medium"
		assert length < 1000, "Rowdy list for size " + size_name + " must not be greater than 1000"
	else:
		assert length < 100, "Rowdy list for size " + size_name + " must not be greater than 100"
except ValueError:
	print("Invalid Input... Input should be integers of form: graph_size rowdylist_size")
""""""

def generate_graph(size):
	# g = nx.Graph()
	edges = random.randint(size-1,  (size * (size-1))//2)
	# nodes = [x for x in range(1, size+1)]
	# g.add_nodes_from(nodes)
	# listOfEdges = random.sample(range(1, size+1), 10)
	# #Create a list of tuples#
	# listOfPairEdges = list(zip(listOfEdges[0::2], listOfEdges[1::2]))
	# # print(listOfPairEdges)
	# g.add_edges_from(listOfPairEdges)
	# # print(g.number_of_edges())
	G = nx.gnm_random_graph(size, edges)
	nx.write_adjlist(G, sys.stdout.buffer)
	nx.write_gml(G, './'+size_name+'/input/graph.gml')

"""
Randomly generate a length amount of sets of rowdylists  
"""
def generate_rowdylist(length):

	file = open('./'+size_name+'/input/parameters.txt', "w")
	file.write("4 \n") ##number of buses
	file.write(str(size //4)+"\n") ##size of buses
	for i in range(length):
		setSize = random.randint(0, size-1)
		rowdyList = random.sample(range(size), setSize)
		file.write(str(rowdyList)+"\n")
	file.close()
generate_graph(size)
generate_rowdylist(length)