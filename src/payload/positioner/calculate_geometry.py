from ortools.sat.python import cp_model

class BlockGraph:
    def __init__(self):
        self._start = None
        self._blocks = {}
        self._intersections = []

    def _add_block(self, new):
        if new not in self._blocks:
            self._blocks[new] = Block(new)
        if not self._start:
            self._start = self._blocks[new]

    def add_neighbors(self, name, neighbors):
        self._add_block(name)
        for neighbor in neighbors:
            self._add_block(neighbor)
            self._blocks[name].new_outbound(self._blocks[neighbor])
            self._blocks[neighbor].new_inbound(self._blocks[name])

    def assign_colors(self, block, color):
        if block._color == None:
            block.set_color(color)
            block.update_degree()
            if block._degree > 2 and block not in self._intersections:
                self._intersections.append(block)

            for neighbor in block._outbound:
                self.assign_colors(neighbor, not color)
            for neighbor in block._inbound:
                self.assign_colors(neighbor, not color)

    def __str__(self):
        return str(self._blocks.values())

    def __repr__(self):
        return self.__str__()

class Block:
    def __init__(self, name):
        self._color = None
        self._outbound = []
        self._inbound = []
        self._name = name
        self._degree = 0

    def set_color(self, c):
        self._color = c

    def color(self):
        return self._color

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
        return f"{self._name}:{1 if self._color == True else 0 if self._color == False else '!'}"

    def __repr__(self):
        return self.__str__()



def calculate_extras(requirements):
    # Optimize for least amount of extras given an optional extra at every intersection

    model = cp_model.CpModel()

    graph = BlockGraph()
    graph.add_neighbors("1",["2"])
    graph.add_neighbors("2",["3"])
    graph.add_neighbors("3",["1"])
    graph.add_neighbors("2",["2a"])
    graph.add_neighbors("2a",["2b"])
    graph.add_neighbors("a",["1"])
    graph.assign_colors(graph._start, False)
    print(graph)

    # Add data

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    # Statistics.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        pass

    else:
        pass

if __name__ == "__main__":
    calculate_extras("")
