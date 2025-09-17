import xgi

################ Generate random hypergraphs: 
#Described as ‘random hypergraph’ by M. Dewar et al. in https://arxiv.org/abs/1703.07686

"""
Parameters
:
N (int) – Number of nodes

ps (list of float) – List of probabilities (between 0 and 1) to create a hyperedge at each order d between any d+1 nodes.
For example, ps[0] is the wiring probability of any edge (2 nodes), ps[1] of any triangles (3 nodes).

order (int of None (default)) – If None, ignore. If int, generates a uniform hypergraph with edges of order order (ps must have only one element).

seed (integer or None (default)) – Seed for the random number generator.

NOTE 1: This hyper-graph generator is not for simple hyper-graphs. This means that there could be an edge that is a subset of another edge.
NOTE 2: This hyper-graph generator produces non-linear hypergraphs. This means that hyper-edges can intesect with one or more nodes.

"""

#n = 20
ps = [0.01, 0.01, 0.01]  # hypergraph rank = len(ps) + 1
#rank = len(ps) + 1

# H = xgi.random_hypergraph(n, ps, order = None, seed = 0)

# # playing with H
# print("Number of nodes: ", len(H.nodes))
# print("Number of edges: ", len(H.edges))

n = 1000
ps = [0.00015, 0.00015]  # hypergraph rank = len(ps) + 1

for _ in range(7):
    H = xgi.fast_random_hypergraph(n, ps, order = None, seed = 0)
    ps = [p * 1.1 for p in ps]
    print("Number of nodes: ", len(H.nodes), "ps = ", ps,  "Number of edges: ", len(H.edges))
    name_string = "C:\\Users\\ismai\\MIS_HGs_codes\\LargeHyperGraphsRank3\\" + "n" + str(n) + "_m" + str(len(H.edges))+".json"
    xgi.write_json(H, name_string)
    

