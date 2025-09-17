import torch 
import xgi
import time
from checkers import IS_checker, MaxIS_checker
from gradient import gradient_function
from utils import relabel_hypergraph_nodes_to_int
import pickle

print("Hello Ismail")

################ Generate graph: 

#n = 120
#ps = [0.0002, 0.0002, 0.0002] # hypergraph rank = len(ps) + 1
#rank = len(ps) + 1

#H = xgi.random_hypergraph(n, ps, order = None, seed = 0)
# H = xgi.random_hypergraph(n, ps, order=None, seed=0)
H = xgi.read_json("C:\\Users\\ismai\\MIS_HGs_codes\\HyperGraphs\\n100_m727.json")
H = relabel_hypergraph_nodes_to_int(H)
n = len(H.nodes)

# playing with H
print("Number of nodes: ", len(H.nodes))
print("Number of edges: ", len(H.edges))


list_of_edges = []

for edge in H.edges:
  #print("Edge: ", edge, " has nodes: ", H.edges.members(edge))
  list_of_edges.append(list(H.edges.members(edge)))



start = time.time()
# initial vector:
#torch.manual_seed(1)

# lets code degree-based intialization:
degrees = dict(H.degree())   # this is a dictionary
deg_values = torch.tensor(list(degrees.values()), dtype=torch.float32)  # convert to tensor
max_deg = torch.max(deg_values) # maximum degree
# normalize the degrees to be between 0 and 1:
deg_values = (deg_values ) / (max_deg) # now between 0 and 1
deg_values = 1 - deg_values # we want to start with low-degree nodes having high values
x_n = deg_values / torch.max(deg_values) # normalize to have max value = 1


step_size = 0.15
number_of_iter = 10000
gamma = 5
momentum_param = 0.5
exploration_parameter = 5
vel = torch.zeros(n)

time_limit = 60 # in seconds

best_MIS_size = 0
best_vector = x_n.clone()

for iter in range(number_of_iter):
  if time.time() - start > time_limit:
    break

  grad = gradient_function(list_of_edges,x_n,gamma)
  vel = momentum_param * vel + grad
  x_n = x_n - step_size * vel
  # clippin the updated x to be within [0,1]
  x_n = torch.clamp(x_n, 0, 1)
  # check for MIS on a binarized version of x_n:
  z_n = x_n.clone()
  z_n[z_n > 0] = 1
  z_n[z_n == 0] = 0
  set_to_check = [i for i, v in enumerate(z_n) if v != 0]
  #print("this is x_n", x_n)
  if IS_checker(set_to_check, H) == True: # This checks for no violations (no hyper-edge is fully contained)
    if MaxIS_checker(set_to_check, H) == True: # This checks for maximality
      if len(set_to_check) > best_MIS_size:
        best_MIS_size = len(set_to_check)
        best_vector = z_n
      print("Iter: ", [iter], "Current MaxIS_size = ", [len(set_to_check)], "Best MaxIS_size = ", best_MIS_size) 

      x_n = x_n +  exploration_parameter*torch.randn_like(x_n)
      x_n = torch.clamp(x_n, 0, 1)

end = time.time() 

print("Best MaxIS_size = ", [best_MIS_size])
print(f"Run-time: {end - start:.6f} seconds")
with open("x_test.pkl", "wb") as f:
    pickle.dump(best_vector, f)

print(best_vector)
