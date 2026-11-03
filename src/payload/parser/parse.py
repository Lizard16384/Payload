import re

class Coord:
    def __init__(self, x, y, z):
        self.update(x, y, z)

    def update(self, x, y, z):
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
        elif isinstance(value, int):
            return float(value)
        elif not isinstance(value, str):
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
        if self._id == 0:
            if offset != 0:
                raise ValueError(f"Cannot reference within groups before incrementing! ({offset} from {self._name}, which is currently undefined)")
            return self._name
        
        val = self._id + offset
        name = self._name + str(val)
        if val < 1:
            raise ValueError(f"Block {name} does not exist!")
        else:
            return name
    
    def increment(self, num=1):
        self._id += num

class ParseData:
    def __init__(self, type, data):
        self.type = type
        self.data = data

class Parser:
    def __init__(self, action_data):
        self.lines = []
        self.parsing = []
        self.coordinates = {}
        self.origin = Coord(0,0,0)
        self.raw_data = {}
        for new in action_data:
            if new.type == "positions":
                for key, value in new.data.items():
                    self.coordinates[key] = value
            elif new.type == "raw_data":
                for key, value in new.data.items():
                    self.raw_data[key] = value

        self.groups = {}
        self.aliases = {}

    def new_line(self):
        self.lines.append(self.parsing)
        self.parsing = []
    
    def add_string(self, string):
        self.parsing.append(string)

    def add_raw_data(self, name):
        self.parsing.append(self.raw_data[name])

    def add_alias(self, original, alias):
        self.coordinates[self.eval_name(alias)] = self.coordinates[self.eval_name(original)]

    def add_relative_offset(self, name1, name2):
        self.parsing.append(Action("pos", self.eval_name(name1), self.eval_name(name2)))

    def add_relative_direction(self, name1, name2):
        self.parsing.append(Action("dir", self.eval_name(name1), self.eval_name(name2)))

    def update_coord(self, name, coordinates):
        name = self.eval_name(name)
        if name not in self.coordinates:
            self.coordinates[name] = Coord(coordinates[0], coordinates[1], coordinates[2])
        else:
            self.coordinates[name].update(coordinates[0], coordinates[1], coordinates[2])

    def get_answer(self, action):
        if action.type == "pos":
            if not action.name1: # From 0 0 0
                answer = str(self.coordinates[action.name2])
            elif not action.name2: # To 0 0 0
                answer = str(self.coordinates[action.name1] * -1)
            else:
                answer = str(self.coordinates[action.name2] - self.coordinates[action.name1])
        elif action.type == "dir":
            answer = self.coordinates[action.name1].direction(self.coordinates[action.name2])
        return answer

    def eval_name(self, raw):
        if raw is None:
            return
        data = re.search(r"^(\d*(?=\+))?(\+?)(.*?)(\d*?)([-+]\d*)?$", raw)
        incr = 0 if data.group(1) == None and data.group(2) == "" \
                else 1 if data.group(1) == "" and data.group(2) == "+" \
                else int(data.group(1))
        id = data.group(4)
        name = data.group(3)
        delta = 0 if data.group(5) == None \
                else 1 if data.group(5) == "+" \
                else -1 if data.group(5) == "-" \
                else int(data.group(5))

        if id != "":
            if data.group(2) != "" or data.group(5) != None:
                raise ValueError(f"Numbers at the end name of {data.group(0)} is not understood alongsied group-scope modifiers")
            return name + id
        if name not in self.groups:
            self.groups[name] = GroupName(name)

        self.groups[name].increment(incr)
        return self.groups[name].get_name(delta)

    def final(self):
        final = []
        if self.parsing:
            self.new_line()
        for item in self.lines:
            line = ""
            for subitem in item:
                if type(subitem) == str:
                    line += subitem
                elif type(subitem) == Action:
                    line += self.get_answer(subitem)
            final.append(line)
        return final

class Action:
    def __init__(self, type, name1, name2):
        self.type = type
        self.name1 = name1
        self.name2 = name2



def split_by_actions(line, delimeter=("$(",")")):
    """
    Takes a line and splits it up into a list separated with actions
    Thus, every other item in the new list is an action

    Supports custom start and end sequences. Default is $(data).
    Anything should work as long as every occurence of it is only used as an action
    If for some reason it is not sufficient, a backslash before will ignore it as an action.
    """
    start, end = re.escape(delimeter[0]), re.escape(delimeter[1])
    split_line = []
    working_index = 0
    for action in re.finditer(f"{start}.*?{end}",line):  # regex to find actions
        # negative lookbehind for backslash is not used as backslash needs to be removed
        # later anyways and it's convenient to do so while actions are being read
        split_line.append(line[working_index:action.start()])
        if line[action.start() - 1] == "\\":
            split_line[-1] == split_line[-1][:-1] + action.group()
        else:
            split_line.append("$" + action.group()[2:-1])
        working_index = action.end()
    split_line.append(line[working_index:])
    return split_line



def parse_command(command_lines, parse_data):
    parser = Parser(parse_data)
    block_comment = False
    for line in command_lines:
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

        split_line = split_by_actions(line)

        for string in split_line:  # Process actions
            if len(string) == 0:
                continue
            if string[0] == "$":
                answer_action(string[1:], parser)
            else:
                parser.add_string(string)
        parser.new_line()

    return parser.final()

def answer_action(action, parser):
    if action[0] == "#":
        return
    action_data = action.split(":")
    tag = action_data[0]
    body = action_data[1]
    if tag == "data":
        parser.add_raw_data(body)
        return
    elif tag == "alias":
        names = body.split(",")
        parser.add_alias(names[0], names[1])
        return
    if body[-5:] == "_next":
        body =  f"{body[:-5]},{body[:-5]}+1"

    operations = body.split(",")
    if len(operations) == 1: # Special case of get position from 0 0 0
        parser.add_relative_offset(None, operations[0])
        return

    first = operations[0]
    second = operations[1]

    if tag == "set": # Assign a coordinate
        parser.update_coord(first, operations[1:])
    elif tag == "dir": # from-to local coordinate difference
        parser.add_relative_offset(first, second)
    elif tag == "rot": # local N/S/E/W/U/D
        parser.add_relative_direction(first, second)

def get_parse_positions(position_lines):
    positions = {}
    for line in position_lines:
        if not line:
            continue
        line = line.split(":")
        name = line[0]
        coords = line[1][1:-1].split(",")
        positions[name] = Coord(coords[0], coords[1], coords[2])
    return ParseData("positions", positions)

def get_parse_raw_data(data):
    return ParseData("raw_data", data)
