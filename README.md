This repo is for paper: 
# Finding Independent Sets in Hypergraphs Via Differentiable Optimization

## Requirements: 
- xgi
- torch
- cplex 
- cp-sat

## Hypergraphs:
The rank-4 hypergraphs used in the paper were generated using "generate_graphs.py". 
We use the following probablities of hyperedge creation: 

| $n$     | probability of hyperedge creation per hyperedge size | 
|----------|-----|
| 40    | [0.0050, 0.0050, 0.0050]  | 
| 60      | [0.0010, 0.0010, 0.0010]  | 
| 80    | [0.0003, 0.0003, 0.0003]  | 
| 100  | [0.0001, 0.0001, 0.0001]  | 

The hypergraphs are inside folder "HyperGraphs". 

## Hyper-parameters: 
For our algorihtm, we used the following hyper-parameters: 


| $n$     | $\gamma$ | $\beta$ | $\alpha$ | $\eta$ |
|----------|-----|-|-|-|
| 60      | 2  | 0.5 | 0.15 | 5 | 
| 80    | 2  | 0.5 | 0.15 | 5 | 
| 100  | 5  | 0.5 | 0.15 | 5 | 
