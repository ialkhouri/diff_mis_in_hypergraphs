import cplex

def mis_value_cplex(H, time_limit=None):
    """
    Compute the Maximum Independent Set (MIS) value (size) on a hypergraph H using CPLEX.

    Args:
        H: xgi.Hypergraph (nodes can be arbitrary labels)
        time_limit: Optional[int|float] time limit in seconds for CPLEX

    Returns:
        int: MIS size (best incumbent size if time-limited; exact optimum if solved to optimality)

    Raises:
        RuntimeError: if CPLEX fails to produce any incumbent solution
    """
    # --- map node labels to contiguous indices 0..n-1
    nodes = list(H.nodes)
    n = len(nodes)
    node_to_idx = {v: i for i, v in enumerate(nodes)}

    # --- collect hyperedges as index lists
    list_of_edges = []
    for e in H.edges:
        members = H.edges.members(e)
        idx_edge = [node_to_idx[v] for v in members]
        if len(idx_edge) > 0:
            list_of_edges.append(idx_edge)

    # --- build MILP
    cpx = cplex.Cplex()
    cpx.set_problem_type(cplex.Cplex.problem_type.MILP)
    cpx.set_log_stream(None)
    cpx.set_error_stream(None)
    cpx.set_warning_stream(None)
    cpx.set_results_stream(None)

    # variables x_i in {0,1}
    cpx.variables.add(lb=[0.0]*n, ub=[1.0]*n, types=["B"]*n, names=[f"x_{i}" for i in range(n)])

    # constraints: for each hyperedge e, sum_{v in e} x_v <= |e| - 1
    if list_of_edges:
        rows = []
        senses = []
        rhs = []
        names = []
        for k, edge in enumerate(list_of_edges):
            rows.append(cplex.SparsePair(ind=edge, val=[1.0]*len(edge)))
            senses.append("L")
            rhs.append(len(edge) - 1.0)
            names.append(f"edge_{k}")
        cpx.linear_constraints.add(lin_expr=rows, senses=senses, rhs=rhs, names=names)

    # objective: maximize sum x_i
    cpx.objective.set_sense(cpx.objective.sense.maximize)
    cpx.objective.set_linear([(i, 1.0) for i in range(n)])

    # time limit (seconds)
    if time_limit is not None:
        cpx.parameters.timelimit.set(float(time_limit))

    # solve
    cpx.solve()

    # status and incumbent handling
    # Even with a timeout, CPLEX usually returns a best incumbent. We guard just in case.
    sol_status = cpx.solution.get_status()
    has_incumbent = cpx.solution.is_primal_feasible()

    if not has_incumbent:
        # Fall back: MILP is trivially feasible with all zeros, but if CPLEX didn't return it,
        # signal to the caller that nothing was retrieved.
        raise RuntimeError(f"CPLEX produced no incumbent (status: {sol_status}).")

    # get incumbent objective (integer MIS size)
    mis_val = cpx.solution.get_objective_value()
    return int(round(mis_val))

from ortools.sat.python import cp_model

def mis_value_cpsat(H, time_limit=None):
    """
    Maximum Independent Set (MIS) size for a hypergraph using OR-Tools CP-SAT.

    Args:
        H: xgi.Hypergraph (nodes may be any labels)
        time_limit: Optional[float] solver time limit in seconds

    Returns:
        int: MIS size (best incumbent if time-limited and not proven optimal).
             Returns 0 if no feasible solution is found within the limit (rare).
    """
    # Map node labels to contiguous 0..n-1 indices
    nodes = list(H.nodes)
    n = len(nodes)
    node_to_idx = {v: i for i, v in enumerate(nodes)}

    # Collect hyperedges as lists of indices
    list_of_edges = []
    for e in H.edges:
        members = [node_to_idx[v] for v in H.edges.members(e)]
        if len(members) == 0:
            continue  # empty hyperedges impose no constraint
        list_of_edges.append(members)

    # Build CP-SAT model
    model = cp_model.CpModel()
    x = [model.NewBoolVar(f"x_{i}") for i in range(n)]

    # For each hyperedge e: sum_{v in e} x_v <= |e| - 1  (no hyperedge fully selected)
    for k, edge in enumerate(list_of_edges):
        model.Add(sum(x[v] for v in edge) <= len(edge) - 1).WithName(f"edge_{k}")

    # Objective: maximize number of selected nodes
    model.Maximize(sum(x))

    # Solve
    solver = cp_model.CpSolver()
    if time_limit is not None:
        solver.parameters.max_time_in_seconds = float(time_limit)

    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        # Return the incumbent size
        return int(sum(solver.Value(var) for var in x))
    else:
        # No solution found within limits (very rare for this MILP-like model)
        return 0
