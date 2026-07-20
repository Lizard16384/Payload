class Coord:
    def __init__(self, x, y, z):
        self._x = self.establish(x)
        self._y = self.establish(y)
        self._z = self.establish(z)
    
    def establish(self, value):
        """
        Parses a number according to minecraft's flexible logic
        Accepts and interprets a string, or just uses a float as-is
        Supports omitting decimals and omitting leading zeroes
        """
        if isinstance(value, float):
            return value
        if not isinstance(value, str):
            raise ValueError('Coordinate given is not a string or float!')
        
        number = 0
        string = value.strip("~")
        if string == "":
            number = float(0)
        else:
            if string[0] == ".":
                string = "0" + string
            elif string[0] == "-" and string[1] == ".":
                string = "-0" + string[1:]
            number = float(string)
        return number

    def __add__(self, other):
        new = Coord(self._x, self._y, self._z)
        new._x += other._x
        new._y += other._y
        new._z += other._z
        return new

    def __sub__(self, other):
        new = Coord(self._x, self._y, self._z)
        new._x -= other._x
        new._y -= other._y
        new._z -= other._z
        return new
    
    def __mul__(self, value):
        new = Coord(self._x, self._y, self._z)
        new._x *= value
        new._y *= value
        new._z *= value
        return new

    def no_0(self, value):
        if value == 0:
            return ''
        else:
            string = str(value)
            if string[-2:] == ".0":
                return string[:-2]
            else:
                return string

    def __str__(self):
        return f"~{self.no_0(self._x)} ~{self.no_0(self._y)} ~{self.no_0(self._z)}"
    def __repr__(self):
        return f"Coord({self._x},{self._y},{self._z})"
    
    def taxicab(self):
        return abs(self._x) + abs(self._y) + abs(self._z)
    
    def direction(self, other):
        delta = other - self
        if delta.taxicab() != 1:
            print(self)
            print(other)
            raise ValueError('Direction destination is not adjacent!')
        if delta._x == 1:
            return 'east'
        elif delta._x == -1:
            return 'west'
        elif delta._y == 1:
            return 'up'
        elif delta._y == -1:
            return 'down'
        elif delta._z == 1:
            return 'south'
        elif delta._z == -1:
            return 'north'

class GroupName:
    def __init__(self, name):
        self._name = name
        self._id = 0
    
    def get_name(self, offset):
        return self._name + str(self._id + offset)
    
    def increment(self):
        self._id += 1

class ParseData:
    def __init__(self, type, data):
        self.type = type
        self.data = data



def split_by_actions(line):
    """
    Takes a line and splits it up into a list separated with actions
    Thus, every other item in the new list is an action

    It is rudimentary and very much breaks if you attempt to nest them, but that's alright because there exists no nesting functionality yet
    """
    split_line = []
    action_index = 0
    action_end = 0

    while action_index != -1:
        action_index = line.find("$(",action_end) # Find next action, or quit
        if action_index == -1:
            continue

        # Add the text in between actions before finding the end of the next action
        # Thus it's going from end of last action to start of next action
        split_line.append(line[action_end:action_index])

        action_end = line.find(")",action_end) + 1

        split_line.append("$" + line[action_index + 2 : action_end - 1])
    split_line.append(line[action_end:])
    return split_line

def process_n(name, groups):
    def parse_n(name):
        raw_name, is_n, incr, delta_n = "", False, 0, 0

        pos_of_n = name.rfind("_n")
        if pos_of_n != len(name) - 2 and name[pos_of_n + 2] not in "+-":
            return name, is_n, incr, delta_n
        
        is_n = True
        if name[0] == "+":
            amt = name.rfind("+")
            raw_name = name[amt + 1:pos_of_n]
            incr = amt + 1
        else:
            raw_name = name[:pos_of_n]
        
        delta_str = name[pos_of_n + 2:]
        if len(delta_str) >= 1:
            if delta_str[0] == "+":
                delta_n = int(delta_str[1:])
            else:
                delta_n = int(delta_str)

        return raw_name, is_n, incr, delta_n
    
    raw_name, is_n, incr, delta_n = parse_n(name)
    result_name = raw_name
    if is_n:
        if raw_name not in groups:
            groups[raw_name] = 0
        groups[raw_name] += incr
        result_name = raw_name + str(groups[raw_name] + delta_n)
    return result_name

def parse_position_actions(action, coordinates, groups):

    # assumes already stripped $()
    operations = action.split(":")

    if len(operations) == 1: # Special case of get position from 0 0 0
        return str(coordinates[process_n(action, groups)])

    first = operations[0]
    second = operations[2]
    type = operations[1]

    first = process_n(first, groups)
    second = process_n(second, groups)
    
    if first == second:
        raise ValueError("Both coordinates cannot be the same!")

    if type == "=": # Assign a coordinate
        coords = second.split()
        coordinates[first] = Coord(coords[0], coords[1], coords[2])
        return ""
    
    elif type == "->": # from-to local coordinate difference
        if first == "": # From 0 0 0
            return str(coordinates[second])
        elif second == "": # To 0 0 0
            return str(coordinates[first] * -1)
        return str(coordinates[second] - coordinates[first])
        
    elif type == "~": # local N/S/E/W
        return coordinates[first].direction(coordinates[second])

def read_positions(file_lines):
    positions = {}
    for line in file_lines:
        line = line.split(":")
        name = line[0]
        coords = line[1][1:-1].split(",")
        positions[name] = Coord(coords[0], coords[1], coords[2])
    return positions

def parse_command(command_lines, parse_data):
    positions = {}
    raw_data = {}

    for parse_add in parse_data:
        if parse_add.type == "positions":
            for key, value in parse_add.data.items():
                positions[key] = value
        elif parse_add.type == "raw_data":
            for key, value in parse_add.data.items():
                raw_data[key] = value

    position_groups = {}
    final_data = []
    for line in command_lines:
        block_comment = False
        comment_type = ""
        if len(line) == 0:
            continue
        if line[0] == "#" or line[0:2] == "//":
            continue
        if not block_comment:
            if line[0:4] == '"""':
                block_comment = True
                comment_type = '"""'
                continue
            if line[0:4] == "'''":
                block_comment = True
                comment_type = "'''"
                continue
            if line[0:3] == "/*":
                block_comment = True
                comment_type = "/*"
                continue
        if block_comment:
            if line[0:4] == '"""':
                block_comment = False
                comment_type = ""
            if line[0:4] == "'''":
                block_comment = False
                comment_type = ""
            if line[0:3] == "*/":
                block_comment = False
                comment_type = ""
            continue

        line = split_by_actions(line)
        line_data = []

        for string in line:  # Process actions
            if len(string) == 0:
                continue
            if string[0] == "$":
                if string[1] == "#":
                    continue
                elif string[1] == "~":
                    key = string[2:]
                    if key in raw_data:
                        string = raw_data[key]
                    else:
                        raise Exception("Command expects raw data to be inserted (prefix ~) but no raw data was provided!")
                elif string[1] == "=":
                    aliases = string[2:].split(",")
                    positions[aliases[1]] = positions[process_n(aliases[0],position_groups)]
                    string = ""
                elif string[-5:] == "_next":
                    string = parse_position_actions(f"{string[1:-5]}_n:~:{string[1:-5]}_n+1",positions,position_groups)
                else:
                    string = parse_position_actions(string[1:],positions,position_groups)
            line_data.append(string)
        
        final_data.append("".join(line_data))
    return "".join(final_data)

def get_parse_positions(position_lines):
    positions = {}
    for line in position_lines:
        line = line.split(":")
        name = line[0]
        coords = line[1][1:-1].split(",")
        positions[name] = Coord(coords[0], coords[1], coords[2])
    return ParseData("positions", positions)

def get_parse_raw_data(data):
    return ParseData("raw_data", data)
