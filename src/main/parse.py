"""
Warning: description may be outdated. Will address later.

Uses several custom format implementations in order to automate some
otherwise tedious interactions in all in one commands.

Custom actions are embedded in a $(), unless the string "$(" is required raw,
in which case "\\$(" will ignore what otherwise may have been "$()"

All whitespace at the beginning and end of a line is stripped

Actions will read from lines that dictate the action anywhere in the file.
Actions that assign data but do not otherwise impact the command are as follows:

1) _n
    Any time a Name ends in _n, it is dynamtically incrementing. Primarily, every
    time the entire name is prepended with a "+", that increments the current _n id and then
    uses that value there, i.e. "+A_n" behaves the same as referring to "A_n" while
    also incrementing the id. Any time the entire name is appended with "+<#>" or "-<#>",
    it refers to that many positions back in the _n sequence, i.e. "A_n+1"

2) $(=Name,Name2)
    Adds an alias to Name2. This is particularly useful for adding an alias to
    an _n name, as those are changing as the file is read and you may want
    to refer to one particular block no matter what its processed _n value is.

3) $(Name|Name2:<something>:Name|Name2) Can specify as many aliases as wanted. This is useful if
    you want to automate coordinate placing and sequences with _n, but want to consistently
    refer to the same block afterwards regardless of its _n position.

Actions that directly insert dynamic data where they show up are as follows:
1) $(Name1:->:Name2) Gets the local coordinate change from 1 to 2
    1b) If either 1 or 2 is empty, it is treated as 0 0 0
2) $(Name1:~:Name2) Gets the direction N/S/E/W/U/D going from 1 to 2
    Only intended if the two coordinates are next to each other: it is already
    assumed that they are next to each other in order to get the facing direction.

Shorthand syntax to do same things mentioned above:

1) $(Name__next) is the same as $(Name_n:~:Name_n+1) because it's pretty common to say
    to get the direction of the next in a group.

2) $(Name) : No action is assumed to be retrieving the position, or, $(:->:Name)
"""

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
    
def read_file(file_name):
    file = open(file_name)
    file_lines = file.readlines()
    file.close()
    for i in range(len(file_lines)):
        new = file_lines[i].strip()
        if len(new) > 0 and new[0] == "#":
            file_lines[i] = ""
        else:
            file_lines[i] = new
    return file_lines



def split_by_actions(line):
    """
    Takes a line and splits it up into a list separated with actions
    Thus, every other item in the new list is an action

    It is rudimentary and very much breaks if you attempt to nest them
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

def parse_actions(action,coordinates, groups):

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

def parse_positions(file_lines):
    positions = {}
    for line in file_lines:
        line = line.split(":")
        name = line[0]
        coords = line[1][1:-1].split(",")
        positions[name] = Coord(coords[0], coords[1], coords[2])
    return positions

def process_final(file_lines,coordinates,groups,raw_data):
    final_string = ""
    repeat = False
    for line in file_lines:
        if len(line) == 0:
            continue
        if line[0] == "#":
            continue

        line = split_by_actions(line)
        line_string = ""

        for string in line:  # Process actions
            if len(string) == 0:
                continue
            if string[0] == "$":
                if string[1] == "#":
                    continue
                elif string[1] == "~":
                    string = raw_data[string[2:]]
                elif string[1] == "=":
                    aliases = string[2:].split(",")
                    coordinates[aliases[1]] = coordinates[process_n(aliases[0],groups)]
                    string = ""
                elif string[-5:] == "_next":
                    string = parse_actions(f"{string[1:-5]}_n:~:{string[1:-5]}_n+1",coordinates,groups)
                else:
                    string = parse_actions(string[1:],coordinates,groups)
            line_string = line_string + string
        
        final_string = final_string + line_string
    if not repeat:
        return final_string
    else:
        return process_final([final_string],coordinates,groups)

def parse_command(file_lines,position_lines,raw_data):
    block_positions = parse_positions(position_lines)
    groups = {}
    final_cmd = process_final(file_lines,block_positions,groups,raw_data)
    return final_cmd
