"""
Solve for where extra blocks need to be inserted in order to make an arrangement
of those blocks in a gridspace even possible. The idea behind the limitations
is that it is not possible for certain blocks to be next to each other. In a
chess board, by definition, two black tiles are never next to each other; you
need to insert a white tile to link two black tiles directly. It has to be linked
directly because that's the only way for a chain command block to send its
execution to the next chain.

The convenient property of this is that whenever a new block has to be inserted
to make an arrangement possible, any chain that previously needed to go to a
specific block can now go to either its original block or the extra block
inserted directly before. This eliminates the need to care what color tile
an incoming block is when its destination received an extra block.
"""

from ortools.sat.python import cp_model

from payload.compressor import position_requirements

class BlockGraph:
    def __init__(self):
        self.model = None
        self._start = None
        self._blocks = {}
        self._extras = []

    def _add_block(self, new):
        if new not in self._blocks:
            self._blocks[new] = Block(new)

    def set_start(self, start):
        self._start = self._blocks[start]

    def add_neighbor(self, name, neighbor):
        self._add_block(name)
        self._add_block(neighbor)
        self._blocks[name].new_outbound(self._blocks[neighbor])
        self._blocks[neighbor].new_inbound(self._blocks[name])

    def assign_colors(self, block, color):
        if block._color is None:
            block._color = color
            block.update_degree()

            for group in (block._outbound, block._inbound):
                for neighbor in group:
                    if neighbor._color is None:
                        next_color = self.model.new_bool_var(f"{neighbor._name}")
                        #self.model.add(color != next_color)
                        self.assign_colors(neighbor, next_color)

    def set_requirements(self):
        for block in self._blocks.values():
            if block._degree <= 2:
                for group in (block._outbound, block._inbound):
                    for neighbor in group:
                        if neighbor._degree <= 2:
                            self.model.add(block._color != neighbor._color)
            elif block._degree <= 10:
                block._extra = self.model.new_bool_var(f"{block._name}_extra")
                self._extras.append(block._extra)
                for neighbor in block._outbound:
                    if neighbor._degree <= 2:
                        self.model.add(block._color != neighbor._color)
                for neighbor in block._inbound:
                    # Restrict inbound to opposite color if the extra is not in place
                    restricted = self.model.new_bool_var(f"{block._name}_extra_helper")
                    self.model.add(restricted != block._extra)
                    self.model.add(block._color != neighbor._color).only_enforce_if(restricted)
            else:
                raise Exception(
                    f"Single block '{block._name}' requires more than 10 direct neighbors!"
                    f"Accounting for this is not yet implemented!"
                    )


    def __str__(self):
        return str(self._blocks.values())

    def __repr__(self):
        return self.__str__()

class Block:
    def __init__(self, name):
        self._color = None
        self._extra = None
        self._outbound = []
        self._inbound = []
        self._name = name
        self._degree = 0

    def update_degree(self):
        self._degree = len(self._outbound) + len(self._inbound)

    def new_outbound(self, new):
        if new not in self._outbound:
            self._outbound.append(new)

    def new_inbound(self, new):
        if new not in self._inbound:
            self._inbound.append(new)

    def __iter__(self):
        for neighbor in self._outbound:
            yield neighbor

    def __str__(self):
        return f"{self._name}:{self._color}"

    def __repr__(self):
        return self.__str__()

def add_all_neighbors(graph, data):
    for group in data["groups"]:
        # Order groups next to each other
        for i in range(1, group["amount"]):
            name1 = f"{group["name"]}{i}"
            name2 = f"{group["name"]}{i+1}"
            if {name1, name2} not in data["disconnections"]:
                graph.add_neighbor(name1, name2)
        # Set start and end position dependencies outside of groupings:
        for start in group["start"]:
            graph.add_neighbor(start, f"{group["name"]}1")
        for end in group["end"]:
            graph.add_neighbor(f"{group["name"]}{group["amount"]}", end)
    
    for single in data["individual"]:
        for start in single["start"]:
            graph.add_neighbor(start, single["name"])
        for end in single["end"]:
            graph.add_neighbor(single["name"], end)
    
    for extra in data["extra_connections"]:
        graph.add_neighbor(extra[0], extra[1])

def calculate_extras(requirements, start):
    data, fixed_positions, conditionals, size, origin = requirements
    # Optimize for least amount of extras given an optional extra at every intersection

    model = cp_model.CpModel()

    graph = BlockGraph()
    graph.model = model
    init = model.new_bool_var("Start")
    add_all_neighbors(graph, data)
    graph.set_start(start)
    graph.assign_colors(graph._start, init)
    graph.set_requirements()
    print(graph)

    extras = model.new_int_var(0,len(graph._extras),"num_extras")
    model.add(sum(graph._extras) <= extras)
    model.minimize(extras)

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    # Statistics.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("PASSED")
        print(f"Extra blocks inserted: {solver.value(extras)}")
        for item in graph._extras:
            if solver.value(item) == 1:
                for changed in graph._blocks[item.name.removesuffix('_extra')]._inbound:
                    print(f"{changed._name} destination now {item.name}")

    else:
        print("FAILED")

if __name__ == "__main__":
    requirements = position_requirements.return_data()
    calculate_extras(requirements, "init1")
