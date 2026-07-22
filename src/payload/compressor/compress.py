import heapq
import math
import bisect

from importlib import resources
from pathlib import Path

from payload.parser import parse
from payload import finish
from payload.positioner import calculate_positions

class LinkedList():

    def __init__(self):
        self._head = None
        self._tail = None
        self._length = 0
    
    def head(self):
        return self._head
    
    def tail(self):
        return self._tail

    def append(self, node):
        if type(node) == Node:
            new = node
        else:
            new = Node(node)
        
        if self._head == None:
            self._head, self._tail = new, new
        else:
            self._tail.set_next(new)
            new.set_prev(self._tail)
            self._tail = new
        self._length += 1

        return new

    def insert_after(self, node, new_node):
        if type(new_node) == Node:
            new = new_node
        else:
            new = Node(new_node)
        
        if node is self._tail:
            return self.append(new_node)
        else:
            new.set_next(node.next())
            node.next().set_prev(new)
            node.set_next(new)
            new.set_prev(node)
            self._length += 1
            return new
    
    def pop(self, node):
        self._length -= 1
        node._unlinked = True
        if node is self._head and node is self._tail:
            self._head, self._tail = None, None
            return node
        elif node is self._head:
            self._head = node.next()
            self._head.set_prev(None)
            node.set_next(None)
            return node
        elif node is self._tail:
            self._tail = node.prev()
            self._tail.set_next(None)
            node.set_prev(None)
            return node
        else:
            node.prev().set_next(node.next())
            node.next().set_prev(node.prev())
            node.set_next(None)
            node.set_prev(None)
            return node
    
    def add_head(self, node):
        if type(node) == Node:
            new = node
        else:
            new = Node(node)
        
        new.set_next(self._head)
        self._head.set_prev(new)
        self._head = new

    def remove(self):
        return self.pop(self._head)
    
    def sort(self):
        """
        Sorts a list by caching the end node of each unique value. Fast
            for a list with not many unique values but lots of items to be
            sorted.
        """
        amounts = []
        cache = {}
        unsorted = self
        sorted = LinkedList()

        while unsorted._head != None:
            to_sort = unsorted.remove()
            qty = len(to_sort.value()._definition)

            if sorted._head == None:  # first element, new list empty
                cache[qty] = sorted.append(to_sort)
                amounts.append(qty)
            elif qty in cache:  # new is an already seen quantity, add it to the end of where that known quantity is
                cache[qty] = sorted.insert_after(cache[qty], to_sort)
            elif qty not in cache:  # new amount not yet in the list
                i = bisect.bisect_left(amounts, qty)
                if i:
                    cache[qty] = sorted.insert_after(cache[amounts[i-1]], to_sort)
                    amounts.insert(i, qty)
                else:  # new is the now lowest value
                    cache[qty] = sorted.add_head(to_sort)
                    amounts.insert(0, qty)
        unsorted._head = sorted._head

    def __len__(self):
        return self._length
    
    def __str__(self):
        string = ""
        current = self._head
        while current != None:
            string += str(current.value())
            if current.next():
                string += ", "
            current = current.next()
        return "[" + string + "]"

    def __repr__(self):
        return str(self)
    
    def assign_ids(self):
        i = 0
        current = self._head
        while current != None:
            current.set_id(i)
            i += 1
            current = current.next()
    
    def __iter__(self):
        current = self._head
        while current is not None:
            yield current.value()
            current = current.next()
    
    def format_dict(self):
        string = ""
        current = self._head
        while current != None:
            string += str(current.value()._definition)
            if current.next():
                string += ", "
            current = current.next()
        return "[" + string + "]"

class Node():

    def __init__(self, value):
        self._value = value
        self._prev = None
        self._next = None
        self._id = None
        self._unlinked = False
    
    def value(self):
        return self._value
    
    def set_value(self, value):
        self._value = value
    
    def next(self):
        return self._next
    
    def set_next(self, new):
        self._next = new
    
    def prev(self):
        return self._prev
    
    def set_prev(self, new):
        self._prev = new

    def set_id(self, i):
        self._id = i

    def id(self):
        return self._id
    
    def unlinked(self):
        return self._unlinked
    
    def __str__(self):
        return str(self._value)
    
    def __repr__(self):
        return str(self)
    
    def __lt__(self, other):
        return False

class Symbol():

    def __init__(self, definition):
        self._definition = definition
        self._index = None
        self._uses = 0
    
    def uses(self):
        return self._uses

    def incr(self):
        self._uses += 1

    def decr(self):
        self._uses -= 1

    def __str__(self):
        return f"{str(self._definition)}:{str(self._index)}" if self._index is not None else f"{str(self._definition)}:?"
    
    def __repr__(self):
        return str(self)
    
    def __lt__(self, other):  # Necessary for the heap library to do its job
        return False
    

def iterable_to_linked(items, dictionary, dict_lookup):
    lookup = {}
    linked_list = LinkedList()
    for item in items:
        if item not in lookup:
            new = Symbol(item)
            lookup[item] = new
            dict_lookup[new] = dictionary.append(new)
        linked_list.append(lookup[item])
        lookup[item].incr()
    return lookup, linked_list

def create_list_pairs(linked_list):
    data = {"heap":[],"starts":{},"ends":{},"pairs":{},"max":{"list":[],"pair":None,"amount":0}}
    current = linked_list.head()
    previous_pair = None
    while current != None and current.next() != None:
        
        pair = (current.value(), current.next().value())

        # skip every other pair in repeating sequences
        # i.e. "aaa" will register 1 "aa" and "bbbbbb" will register 3 "bb"
        if pair == previous_pair:
            previous_pair = None
            current = current.next()
            continue

        # start tracking new pair
        if pair not in data["pairs"]:
            data["pairs"][pair] = LinkedList()
        
        # add new pair to tracking list
        data["pairs"][pair].append((current, current.next()))

        # track the max pair along the way
        if len(data["pairs"][pair]) > len(data["max"]["list"]):
            data["max"]["list"] = data["pairs"][pair]
            data["max"]["pair"] = pair
            data["max"]["amount"] = len(data["max"]["pair"])

        previous_pair = pair

        current = current.next()

    # initialize starting/ending item tracking
    for pair in data["pairs"].keys():
        if pair[0] not in data["starts"]:
            data["starts"][pair[0]] = set()
        data["starts"][pair[0]].add(pair)
        if pair[1] not in data["ends"]:
            data["ends"][pair[1]] = set()
        data["ends"][pair[1]].add(pair)

        push_pair(data, pair)

    return data



'''
Heap is an efficient way to track the most common pair given one added at each step and some others are changing a bunch.
'''

def push_pair(data, pair):
    heap = data["heap"]
    count = len(data["pairs"][pair])
    first_id = data["pairs"][pair].head().value()[0].id()
    heapq.heappush(heap, (-count, first_id, pair))

def get_max_pair(data):
    heap = data["heap"]
    while heap:
        neg_count, first_id, pair = heap[0]
        if pair not in data["pairs"]:
            heapq.heappop(heap)
            continue
        if len(data["pairs"][pair]) == -neg_count:
            return {"list":data["pairs"][pair],"pair":pair,"amount":len(data["pairs"][pair])}
        heapq.heappop(heap)
    return None



def discard_pair(data, pair):
    data["starts"][pair[0]].discard(pair)
    data["ends"][pair[len(pair) - 1]].discard(pair)
    data["pairs"].pop(pair, None)

def clear_invalid(pairs_list):
    current = pairs_list._head
    while current != None:
        if current.value()[0].unlinked() or current.value()[1].unlinked():
            to_remove = current
            current = current.next()
            pairs_list.pop(to_remove)
            continue
        current = current.next()

def register_pair(data, node1, node2):
    pair_key = (node1.value(), node2.value())
    pair_lookup = (node1, node2)

    # register potentially new pair into lookup list
    if pair_key not in data["pairs"]:
        data["pairs"][pair_key] = LinkedList()
    
    # add this specific pair to lookup list
    data["pairs"][pair_key].append(pair_lookup)

    # register potentially new starting or ending item into lookup
    if pair_key[0] not in data["starts"]:
        data["starts"][pair_key[0]] = set()
    if pair_key[1] not in data["ends"]:
        data["ends"][pair_key[1]] = set()

    # add this specific pair to correct lookup lists
    if pair_key not in data["starts"][pair_key[0]]:
        data["starts"][pair_key[0]].add(pair_key)
    if pair_key not in data["ends"][pair_key[1]]:
        data["ends"][pair_key[1]].add(pair_key)
    
    push_pair(data, pair_key)

def compress_pairs(linked_list, data, dictionary, dict_lookup):
    raw_length = len(linked_list)
    while data["max"]["pair"] is not None and len(data["max"]["list"]) > 1:
        print(f"Creating Pairs: {round((((raw_length - len(linked_list))/raw_length) * 100), 1)}% | Amount found:{data["max"]["amount"]}      ", end="\r", flush=True)

        new_symbol = Symbol(data["max"]["pair"])
        data["max"]["pair"][0].incr()
        data["max"]["pair"][1].incr()
        dict_lookup[new_symbol] = dictionary.append(new_symbol)

        # replace pair for new symbol and store new symbols
        new_nodes = []
        current = data["max"]["list"].head()
        while current != None: # insert new pairs into place and track them
            
            new = linked_list.insert_after(current.value()[1], new_symbol)
            new.set_id(current.value()[0].id())
            new_nodes.append(new)
            new_symbol.incr()

            linked_list.pop(current.value()[0])
            linked_list.pop(current.value()[1])
            data["max"]["pair"][0].decr()
            data["max"]["pair"][1].decr()

            current = current.next()
        
        # remove now-invalid pairs due to pair replacement
        discard_pair(data, data["max"]["pair"])

        for family, key in [(data["starts"], data["max"]["pair"][len(data["max"]["pair"]) - 1]),
                            (data["ends"],   data["max"]["pair"][0])]:
            if key not in family:
                continue
            for value in list(family[key]):
                clear_invalid(data["pairs"][value])
                if len(data["pairs"][value]) == 0:
                    discard_pair(data, value)

        #  register new pairs due to pair replacement
        skip_next = False
        i = 0
        for c_node in new_nodes:
            prev_node = c_node.prev()
            next_node = c_node.next()
            if prev_node and prev_node.value() != c_node.value():
                register_pair(data, prev_node, c_node)
            
            if next_node:
                if not (i + 1 < len(new_nodes) and new_nodes[i + 1] is next_node):
                    skip_next = False
                    register_pair(data, c_node, next_node)
                else:
                    if not skip_next:
                        register_pair(data, c_node, next_node)
                    skip_next = not skip_next
            i += 1
        
        data["max"] = get_max_pair(data)

def compress_dict(dictionary, dict_lookup):
    current = dictionary.head()
    while current != None:
        if type(current.value()._definition) != str:
            new_def = []
            for item in current.value()._definition:
                if item.uses() == 1 and item._definition[0] != "%":
                    if len(item._definition) > 1:
                        for new_item in item._definition:
                            new_def.append(new_item)
                        dictionary.pop(dict_lookup[item])
                        dict_lookup.pop(item)
                    else:
                        new_def.append(item)
                        item.decr()
                    
                else:
                    new_def.append(item)
            if type(new_def) != str:
                new = tuple(new_def)
            else:
                new = new_def[0]
            current.value()._definition = new
            dict_lookup[new] = current
        current = current.next()

def assign_indexes(symbols):
    for i, symbol in enumerate(symbols):
        symbol._index = i
    return i



def int_to_base(n, charset):
    base = len(charset)
    if n == 0:
        return charset[0]
    digits = []
    while n > 0:
        digits.append(charset[n % base])
        n //= base
    return ''.join(reversed(digits)).rjust(2, charset[0])

def base_to_int(s, charset):
    base = len(charset)
    value = 0
    for c in s:
        value = value * base + charset.index(c)
    return value

def dict_str(dictionary, charset):
    prev_length = 0
    literals = []

    string = ""
    for symbol in dictionary:
        new = symbol._definition
        if len(new) == 0:
            continue
        if type(new) == str:
            literals.append(symbol._definition)
        else:
            if len(new) > prev_length:
                string += "00" + str(int_to_base(len(new), charset))
                prev_length = len(new)
            for num in new:
                string += str(int_to_base(num._index, charset))
    return literals, string

def output_str(linked_list, charset):
    string = ""
    for symbol in linked_list:
        string += str(int_to_base(symbol._index, charset))
    return string






def parse_rules_str(rule_str, charset):
    rules = []
    i = 0
    length = 0
    while i < len(rule_str):
        if(base_to_int(rule_str[i:i+2], charset) == 0):
            length = base_to_int(rule_str[i+2:i+4], charset)
            i += 4
        rule = []
        for _ in range(length):
            if i + 2 > len(rule_str):
                raise ValueError(f"Unexpected end of rule_str at index {i}")
            rule.append(base_to_int(rule_str[i:i+2], charset))
            i += 2
        rules.append(rule)
    return rules

def parse_output_str(output_str, charset):
    return [base_to_int(output_str[i:i+2], charset) for i in range(0, len(output_str), 2)]

def decode(literals, rule_str, output_str, charset):
    rules = parse_rules_str(rule_str, charset)
    output = parse_output_str(output_str, charset)

    decodingOutput = output[:]
    outputStrings = []
    
    while decodingOutput:
        val = decodingOutput[0]
        if val > len(literals):
            rule = rules[val - len(literals) - 1]
            for k in range(len(rule)):
                decodingOutput.insert(k + 1, rule[k])
            decodingOutput.pop(0)
        else:
            outputStrings.append(literals[val - 1])
            decodingOutput.pop(0)

    return ''.join(outputStrings)





def get_compressed_data(literals, rules, output, original_input, charset):
    base_definition = []
    for i, char in enumerate(charset):
        if char in "= `~!@#$%^&*()[]{}|;:,.<>/?":  # strings with quotes that cannot be omitted in an SNBT key
            key = f'"{char}"'
        else:  # remaining characters have flexibility in SNBT and you can omit the quotes that say it's a string for a slight optimization in characters used
            key = char
        base_definition.append(f"{key}:{i}")
    base_cmd = "base:{amt:" + str(len(charset)) + ',' + ','.join(base_definition) + "}"

    literals_definition = []
    for char in literals:
        if char in "-+= `~!@#$%^&*()[]{}|;:,.<>/?" or char in "0123456789":  # strings with quotes that cannot be omitted in creating an SNBT value
                                                                             # additionally, numbers being numbers instead of strings messes with text resolution interpretation, so they have to be strings as well
            value = f'"{char}"'
        # the rest have to be escaped properly to fit how it is used in the compressor command
        elif char == '"':
            value = f'"\\\\""'
        elif char == "'":
            value = f'"\\\'"'
        elif char == "\\":
            value = f'"\\\\\\\\"'
        else:  # remaining characters have flexibility in SNBT and you can omit the quotes that say it's a string for a slight optimization in characters used, and they will automatically be interpreted as a string
            value = char
        literals_definition.append(value)
    literals_cmd = "literals:[\"\"," + ','.join(literals_definition) + "]"
    
    compressed_data = base_cmd + "," + literals_cmd + ',rules:"' + rules + '",output:"' + output + '"'

    compressed_length = len(rules) + len(output)
    input_length = len(original_input)
    ratio = compressed_length / input_length if input_length > 0 else float('inf')

    print(f"Final compression: {ratio:.4f} ({compressed_length} compressed / {input_length} original)")
    decoded = decode(literals, rules, output, charset)
    if decoded != original_input:
        raise RuntimeError("Decoded command does not match original input.")

    return compressed_data

def compile_command(input_str):
    CUSTOM_BASE_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-+= `~!@#$%^&*()[]{}|;:,.<>/?" # base-92: excludes ' " \ to avoid issues with minecraft /enchant handling.
                                                                                                                       # % can still be used in the base, but needs to be inserted as text after rule unpacking is done.

    dictionary = LinkedList()
    dict_lookup = {}

    symbols, linked_list = iterable_to_linked(input_str, dictionary, dict_lookup)
    linked_list.assign_ids()

    data = create_list_pairs(linked_list)

    compress_pairs(linked_list, data, dictionary, dict_lookup)
    compress_dict(dictionary, dict_lookup)
    dictionary.add_head(Symbol(""))  # Add one to everything so that 00 can be reserved for special properties
    dictionary.sort()
    max_index = assign_indexes(dictionary)
    #dictionary.remove()
    base_needed = math.ceil(math.sqrt(max_index))
    charset = CUSTOM_BASE_CHARS[0:base_needed + 1]
    literals, dict_string = dict_str(dictionary, charset)
    result = output_str(linked_list, charset)

    raw_data = {"storage":"compressor","scoreboard":"compressor"}
    raw_data["snbt"] = get_compressed_data(literals, dict_string, result, input_str, charset)

    compressor_command_path = resources.files("payload.compressor").joinpath("compressor.mcfunction")
    compressor_lines = finish.read_file_lines(compressor_command_path)

    path = resources.files("payload.compressor") / "positions.txt"
    positions_lines = calculate_positions.calculate(path)  # Verify validity of position arrangement or update for a new arrangement if requirements have changed

    command = parse.parse_command(compressor_lines, [parse.get_parse_positions(positions_lines), parse.get_parse_raw_data(raw_data)])
    return command
