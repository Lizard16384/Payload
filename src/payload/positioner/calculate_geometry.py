from ortools.sat.python import cp_model

def calculate_extras(requirements):
    # Optimize for least amount of extras given an optional extra at every valid place

    model = cp_model.CpModel()

    # Add data

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    # Statistics.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        pass

    else:
        pass
