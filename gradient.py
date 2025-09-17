import torch

# The gradient function needs N(v,e)  = {u\in e such that v,u \in e} which is the neibhor of node v in hyper-edge e:
# The gradient for every node v \in V is -1+ sum_{e\in E} \prod_{u\in N(v,e)} x_u... Here, we need e in E such that v is in e.
# let some edge be e = [1,2]
def N_of_v_in_Hyp_edge_e(v,e):
  # Remore v from the list e if v is in e
  i = e.index(v)
  return e[:i] + e[i+1:]

# test
# print(N_of_v_in_Hyp_edge_e(1,[1,2]))
def gradient_function(list_of_edges,x_n, gamma):
  """
  The input is torch vector of size n, and the hyper graph.
  The output is a vector of size n where every entry is
  """
  n = len(x_n)
  grad = torch.zeros(n)
  for v in range(n):
    #print(v)
    s = 0
    for edge in list_of_edges:
      #print(edge)
      if v in edge:
        prod = 1
        #print(N_of_v_in_Hyp_edge_e(v,edge))
        for u in N_of_v_in_Hyp_edge_e(v,edge):
          prod = prod * x_n[u]
        s = s + prod
    grad[v] = -1 + gamma*s
  return grad


# # test the fucntion:
# x_n = torch.tensor([1,1,1,1])
# print(gradient_function(list_of_edges,x_n))
# # the output should be [1,0,0,0] for an H with n = 4 and E = {{1,2},{0,1,3}}