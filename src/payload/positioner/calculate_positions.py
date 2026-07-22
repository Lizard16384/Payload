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
from payload import finish

"""
Calculating if a layout is possible by limitation of amount of blocks allocated to get from one place to another.
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
"""

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

def new_block(model, group, name, size, dims, positions, fixed_positions, intersection_groups):
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
    
    new_pos = (positions[name + "_x"] * dims[1] + positions[name + "_y"]) * dims[2] + positions[name + "_z"]
    if "intersect" not in group:
        intersection_groups["0"].append(new_pos)
    else:
        new_ids = group["intersect"] if type(group["intersect"]) == list else [group["intersect"]]
        for intersect_id in new_ids:
            id = str(intersect_id)
            if id not in intersection_groups:
                intersection_groups[id] = []
            intersection_groups[id].append(new_pos)

def get_all_names(data):
    names = []
    for group in data["groups"]:
        for i in range(1, group["amount"] + 1):
            names.append(f"{group["name"]}{i}")
    for single in data["individual"]:
        names.append(single["name"])
    return names

def get_new_solution(requirements, path):
    print("Previous (or nonexistent) positions no longer satisfy positional requirements. Calculating new positions.")
    new_solution = calculate(requirements)
    print(f"New solution found. Writing to path. ({path})")
    path.write_text("\n".join(new_solution) + "\n")
    return new_solution

def calculate(requirements, *path):
    data, fixed_positions, conditionals, size, origin = requirements
    locked_fixed_positions = {}
    for key, value in fixed_positions.items():
        locked_fixed_positions[key] = value
    original_requirements = data, locked_fixed_positions, conditionals, size, origin
    size_x = size["x"]
    size_y = size["y"]
    size_z = size["z"]
    dims = [size_x, size_y, size_z]

    existing_solution = (finish.read_file_lines(path[0]) if path[0].exists() else None) if path else None

    if existing_solution is not None:
        old_names = get_all_names(data)
        new_names = []

        for line in existing_solution:
            axes = set("+-")
            if line[0:6] == "corner" and set(line[6:9]).issubset(axes):
                continue
            line = line.split(":")
            name = line[0]
            coords = line[1][1:-1].split(",")
            raw_coords = [int(coords[0]) + origin[0], int(coords[1]) + origin[1], int(coords[2]) + origin[2]]
            fixed_positions[name] = raw_coords
            new_names.append(name)

            if raw_coords[0] < 0 or raw_coords[0] > dims[0] \
                or raw_coords[1] < 0 or raw_coords[1] > dims[1] \
                or raw_coords[2] < 0 or raw_coords[2] > dims[2]:
                return get_new_solution(original_requirements, path[0])

        old_names.sort()
        new_names.sort()
    elif path:
       return get_new_solution(original_requirements, path[0])

    # Constraint programming engine
    model = cp_model.CpModel()


    
    positions = {}  # Name of each variable the model tracks, one for x y and z
    relative_dist = {}
    intersection_groups = {"0":[]}

    # Assign everything an x y and z variable
    # Then create a value unique to its position in the grid
    for group in data["groups"]:
        for i in range(1, group["amount"] + 1):
            name = f"{group["name"]}{i}"
            new_block(model, group, name, size, dims, positions, fixed_positions, intersection_groups)

    for single in data["individual"]:
        name = single["name"]
        new_block(model, group, name, size, dims, positions, fixed_positions, intersection_groups)



    # Prevent overlap from everything within specified groups, including a default main group
    for group in intersection_groups.values():
        model.add_all_different(group)



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

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if existing_solution is None:
        # Statistics.
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            """
            print("\nStatistics")
            print(f"  status   : {solver.status_name(status)}")
            print(f"  conflicts: {solver.num_conflicts}")
            print(f"  branches : {solver.num_branches}")
            print(f"  wall time: {solver.wall_time} s")
            print("Values (wrote to file positions.txt):")
            """
            result = {}
            output_lines = []
            for key, value in positions.items():
                coord = [key[0:-2],key[-1]]
                if coord[0] not in result:
                    result[coord[0]] = {}
                result[coord[0]][coord[1]] = value
            for key, value in result.items():
                coord = f"{key}:({solver.value(value["x"]) - origin[0]},{solver.value(value["y"]) - origin[1]},{solver.value(value["z"]) - origin[2]})"
                output_lines.append(coord)
            
            # write corners in
            output_lines.append("")
            for x in [0,dims[0] - 1]:
                for y in [0,dims[1] - 1]:
                    for z in [0,dims[2] - 1]:
                        corner = ("+" if x else "-") \
                            + ("+" if y else "-") \
                            + ("+" if z else "-")
                        name = "corner" + corner
                        coord = f"{name}:({x - origin[0]},{y - origin[1]},{z - origin[2]})"
                        output_lines.append(coord)

        else:  # No solution was possible with new requirements
            raise Exception(
                f"No solution found for requirements given."
                f"Cannot write a new default solution for changed requirements."
            )

        return output_lines
    else:  # A solution is being tested, not generated
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            if old_names != new_names:  # Solution was valid but mismatched names were found, get a new solution
                return get_new_solution(original_requirements, path[0])
            return existing_solution  # Solution was valid without mismatched names
        else:
            return get_new_solution(original_requirements, path[0])  # Solution was not valid, get a new solution
