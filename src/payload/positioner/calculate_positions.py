"""Spatial organization of a path

Given names and numbers of nodes in that name, assume they should be placed
sequentially. Then respect additional custom neighboring requirements and
fixed position requirements in a shape of customizable bounds.

In addition, dummy nodes are automatically added in order to make exact
alignment possiblewhere the intended neighbor is always otherwise a minimum 1
extra node away.
# doesn't do this yet

It is also possible to fix positions of nodes, effectively making it possible
to attempt to fit the nodes into any shape, or simply having a desired
location for a node.
"""

from ortools.sat.python import cp_model
from layouts.compressor import *

def add_neighbor(model, variables, dims, name1, name2):
    x1 = variables[name1 + "_x"]
    x2 = variables[name2 + "_x"]
    y1 = variables[name1 + "_y"]
    y2 = variables[name2 + "_y"]
    z1 = variables[name1 + "_z"]
    z2 = variables[name2 + "_z"]

    dx = model.new_int_var(0, dims[0] - 1, f"{name1},{name2}dx")
    dy = model.new_int_var(0, dims[1] - 1, f"{name1},{name2}dy")
    dz = model.new_int_var(0, dims[2] - 1, f"{name1},{name2}dz")
    model.add_abs_equality(dx, x2 - x1)
    model.add_abs_equality(dy, y2 - y1)
    model.add_abs_equality(dz, z2 - z1)
    model.add(dx + dy + dz == 1)
    return [dx, dy, dz]

def calculate_extras(data):
    # assumes one place that does not have a fixed starting point, or if it does, it's not fixed next to a different block
    evens = []
    odds = []
    even = None
    for group in data["groups"]:
        if not group["start"]:
            even = True
        else:
            even = group["start"][0] in odds
        for i in range(len(group["amount"])):
            if even:
                evens.append(group["name"] + str(i + 1))
            else:
                odds.append(group["name"] + str(i + 1))
            even = not even
        

def new_block(model, name, size, dims, positions, fixed_positions):
    for dim, length in size.items():
        if name in fixed_positions:
            j = 0
            for dim in size.keys():
                coord = name + "_" + dim
                value = fixed_positions[name][j]
                int_var = model.new_int_var(value, value, coord)
                positions[coord] = int_var
                j += 1
            continue
        coord = name + "_" + dim
        int_var = model.new_int_var(0, length - 1, coord)
        positions[coord] = int_var
    
    return (positions[name + "_x"] * dims[1] + positions[name + "_y"]) * dims[2] + positions[name + "_z"]


def main() -> None:

    data, fixed_positions, conditionals, size, origin = return_data()

    # Constraint programming engine
    model = cp_model.CpModel()


    size_x = size["x"]
    size_y = size["y"]
    size_z = size["z"]
    dims = [size_x, size_y, size_z]
    
    positions = {}
    positions_ids = []
    all_positions_ids = {}
    relative_dist = {}

    # Assign everything an x y and z variable
    # Then create a value unique to its position in the grid
    for group in data["groups"]:
        for i in range(1, group["amount"] + 1):
            name = f"{group["name"]}{i}"
            new_pos = new_block(model, name, size, dims, positions, fixed_positions)
            if name not in data["no_fill_space"]:
                positions_ids.append(new_pos)
            all_positions_ids[name] = new_pos
    
    for single in data["individual"]:
        name = single["name"]
        new_pos = new_block(model, name, size, dims, positions, fixed_positions)
        if name not in data["no_fill_space"]:
            positions_ids.append(new_pos)
        all_positions_ids[name] = new_pos

    
    # Ensure no overlap between objects that aren't said to not fill space
    model.add_all_different(positions_ids)

    # add other non-overlaps that are manually specified
    for intersection_group in data["extra_no_intersect"]:
        new_positions_ids = []
        for name in intersection_group:
            new_positions_ids.append(all_positions_ids[name])
        model.add_all_different(new_positions_ids)



    # Rules to place everything next to what it should be:
    for group in data["groups"]:
        # Order groups next to each other
        for i in range(1, group["amount"]):
            name1 = f"{group["name"]}{i}"
            name2 = f"{group["name"]}{i+1}"
            if {name1, name2} not in data["disconnections"]:
                relative_dist[f"{name1} {name2}"] = \
                add_neighbor(model, positions, dims, name1, name2)
        # Set start and end position dependencies outside of groupings:
        for start in group["start"]:
            relative_dist[f"{start} {group["name"]}1"] = \
            add_neighbor(model, positions, dims, start, f"{group["name"]}1")
        for end in group["end"]:
            relative_dist[f"{group["name"]}{group["amount"]} {end}"] = \
            add_neighbor(model, positions, dims, f"{group["name"]}{group["amount"]}", end)
    
    for single in data["individual"]:
        for start in single["start"]:
            relative_dist[f"{start} {single["name"]}"] = \
            add_neighbor(model, positions, dims, start, single["name"])
        for end in single["end"]:
            relative_dist[f"{single["name"]} {end}"] = \
            add_neighbor(model, positions, dims, single["name"], end)
    
    for extra in data["extra_connections"]:
        relative_dist[f"{extra[0]} {extra[1]}"] = \
        add_neighbor(model, positions, dims, extra[0], extra[1])



    # Add conditional straight lines
    # Done after giving neighbors to everything, so that distances to
    # neighbors are already known
    for line in conditionals:
        x_align = model.new_bool_var("x_align")
        y_align = model.new_bool_var("y_align")
        z_align = model.new_bool_var("z_align")
        model.add_exactly_one([x_align, y_align, z_align])
        for i in range(0, len(line) - 1):
            dx = relative_dist[f"{line[i]} {line[i+1]}"][0]
            dy = relative_dist[f"{line[i]} {line[i+1]}"][1]
            dz = relative_dist[f"{line[i]} {line[i+1]}"][2]

            model.add(dy == 0).only_enforce_if(x_align)
            model.add(dz == 0).only_enforce_if(x_align)

            model.add(dx == 0).only_enforce_if(y_align)
            model.add(dz == 0).only_enforce_if(y_align)

            model.add(dx == 0).only_enforce_if(z_align)
            model.add(dy == 0).only_enforce_if(z_align)
    
    # horribly inefficient way to handle relative offsets:
    for offset in data["offsets"]:
        name = f"{offset["from"]} {offset["to"]}"
        if name not in data["offsets"]:
            relative_dist[name] = [
                model.new_int_var(0, dims[0] - 1, f"{offset["from"]},{offset["to"]}dx"),
                model.new_int_var(0, dims[1] - 1, f"{offset["from"]},{offset["to"]}dy"),
                model.new_int_var(0, dims[2] - 1, f"{offset["from"]},{offset["to"]}dz")
            ]

        dx = relative_dist[name][0]
        dy = relative_dist[name][1]
        dz = relative_dist[name][2]
        model.add(dx == positions[offset["to"] + "_x"] - positions[offset["from"] + "_x"])
        model.add(dy == positions[offset["to"] + "_y"] - positions[offset["from"] + "_y"])
        model.add(dz == positions[offset["to"] + "_z"] - positions[offset["from"] + "_z"])
        model.add(dx == offset["offset"][0])
        model.add(dy == offset["offset"][1])
        model.add(dz == offset["offset"][2])

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    
    # Solve.
    status = solver.solve(model)
    
    # Statistics.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("\nStatistics")
        print(f"  status   : {solver.status_name(status)}")
        print(f"  conflicts: {solver.num_conflicts}")
        print(f"  branches : {solver.num_branches}")
        print(f"  wall time: {solver.wall_time} s")
        print("Values (wrote to file positions.txt):")
        result = {}
        for key, value in positions.items():
            coord = [key[0:-2],key[-1]]
            if coord[0] not in result:
                result[coord[0]] = {}
            result[coord[0]][coord[1]] = value
        file_name = "positions.txt"
        file = open(file_name, "w")
        for key, value in result.items():
            coord = f"{key}:({solver.value(value["x"]) - origin[0]},{solver.value(value["y"]) - origin[1]},{solver.value(value["z"]) - origin[2]})"
            print(coord)
            file.write(coord + "\n")
        file.close()
    else:
        print("No solution found.")

"""
add to positions.txt after:
corner1:(-2,-2,-2)
corner2:(2,1,2)
"""

if __name__ == "__main__":
    main()


"""
TEST CODE FOR OPTIMIZATION THAT MAY OR MAY NOT WORK:

def add_manhattan_neighbor_constraint(model, x1, y1, z1, x2, y2, z2, edge_var, M=100):
    '''
    Adds a constraint that (x2,y2,z2) is a Manhattan neighbor of (x1,y1,z1)
    only if edge_var is True. Uses the Big M method to avoid AddAbsEquality.
    '''
    # Create boolean variables for the sign of the difference on each axis
    dx_pos = model.NewBoolVar('dx_pos')
    dy_pos = model.NewBoolVar('dy_pos')
    dz_pos = model.NewBoolVar('dz_pos')

    # Use 'edge_var' as an enabler with Big M
    # If edge_var is 0 (no edge), the constraints are inactive.
    # If edge_var is 1 (edge exists), the following must hold:
    
    # |x1-x2| + |y1-y2| + |z1-z2| == 1
    # This is broken down by the sign variables.
    
    # Sum of absolute differences must be 1 if edge exists
    model.Add((x1 - x2) + (y1 - y2) + (z1 - z2) - 2*(dx_pos*(x1-x2) + dy_pos*(y1-y2) + dz_pos*(z1-z2)) == 1).OnlyEnforceIf(edge_var)
    
    # Link sign variables to the actual differences (Big M constraints)
    model.Add(x1 - x2 >= 0).OnlyEnforceIf(dx_pos)
    model.Add(x1 - x2 < 0).OnlyEnforceIf(dx_pos.Not())
    model.Add(y1 - y2 >= 0).OnlyEnforceIf(dy_pos)
    model.Add(y1 - y2 < 0).OnlyEnforceIf(dy_pos.Not())
    model.Add(z1 - z2 >= 0).OnlyEnforceIf(dz_pos)
    model.Add(z1 - z2 < 0).OnlyEnforceIf(dz_pos.Not())

# Example usage
model = cp_model.CpModel()
x1 = model.NewIntVar(0, 10, 'x1')
y1 = model.NewIntVar(0, 10, 'y1')
z1 = model.NewIntVar(0, 10, 'z1')
x2 = model.NewIntVar(0, 10, 'x2')
y2 = model.NewIntVar(0, 10, 'y2')
z2 = model.NewIntVar(0, 10, 'z2')
edge = model.NewBoolVar('edge')

add_manhattan_neighbor_constraint(model, x1, y1, z1, x2, y2, z2, edge)

"""
