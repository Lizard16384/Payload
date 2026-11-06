from importlib import resources
from pathlib import Path

from payload.parser import parse
from payload import finish
from payload.positioner import calculate_positions
from payload.compressor import position_requirements
from payload.compressor import pair



def linear_remap(num, operation, change_remap = [], remap_to = {}, remap_from = {}):
    if change_remap:  # Editing default values of the function
        i = 0
        for group in change_remap:
            for j in range(group[0], group[1] + 1):
                remap_to[i] = j
                i += 1
        for key, value in remap_to.items():
            remap_from[value] = key
        return
    
    # operation True means the number is already in the range and is to be mapped back starting at 0
    # operation false means the number is first being mapped into the range
    if operation:  # remap number from within the range to raw values
        return remap_from[num]
    else:  # remap raw values to within the range
        return remap_to[num]

def custom_base(val, commons={}):
    if type(val) == int:
        return chr(linear_remap(val, False))
    elif type(val) == str:
        return linear_remap(ord(val), True)

def dict_str(dictionary):
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
                string += custom_base(0) + custom_base(len(new))
                prev_length = len(new)
            for num in new:
                string += custom_base(num._index)
    return literals, string

def output_str(linked_list):
    string = ""
    for symbol in linked_list:
        string += custom_base(symbol._index)
    return string

def parse_rules_str(rule_str):
    rules = []
    i = 0
    length = 0
    while i < len(rule_str):
        if(custom_base(rule_str[i:i+1]) == 0):
            length = custom_base(rule_str[i+1:i+2])
            i += 2
        rule = []
        for _ in range(length):
            rule.append(custom_base(rule_str[i:i+1]))
            i += 1
        rules.append(rule)
    return rules

def parse_output_str(output_str):
    return [custom_base(output_str[i:i+1]) for i in range(0, len(output_str), 1)]

def decode(literals, rule_str, output_str):
    rules = parse_rules_str(rule_str)
    output = parse_output_str(output_str)

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

def get_compressed_data(dictionary, compressed, original_input):
    dictionary.add_head(pair.Symbol(""))  # Add one to everything so that 00 can be reserved for special properties
    max_index = pair.assign_symbol_ids(dictionary)
    
    literals, rules = dict_str(dictionary)
    output = output_str(compressed)

    base_cmd = f'base:"{"".join([chr(linear_remap(i, False)) for i in range(max_index + 1)])} "'  # Extra (space) character needed to allow substring indeces 0 to 1 always valid in /data

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
    print("Verifying integrity of command.")
    decoded = decode(literals, rules, output)
    if decoded != original_input:
        raise RuntimeError("Decoded command does not match original input.")

    return compressed_data

def compile_command(input_str):
    USABLE_ASCII = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-+= `~!@#$%^&*()[]{}|;:,.<>/?" # base-92: excludes ' " \ to avoid issues with minecraft /enchant handling.
    linear_remap(0,"",[[0x1390,0x2000],[0x206F,0xD7FF],[0xE000,0xFFFF]])  # Initialize default values in the function for desired ranges - exclude range of some formatting characters and surrogates.

    dictionary, compressed = pair.re_pair(input_str)

    raw_data = {"storage":"compressor","scoreboard":"compressor"}
    raw_data["snbt"] = get_compressed_data(dictionary, compressed, input_str)

    print("Command compressed. Parsing into compressor command...")

    compressor_command_path = resources.files("payload.compressor").joinpath("compressor.mcfunction")
    compressor_lines = finish.read_file_lines(compressor_command_path)

    path = resources.files("payload.compressor") / "positions.txt"
    requirements = position_requirements.return_data()
    positions_lines = calculate_positions.calculate(requirements, path)  # Verify validity of position arrangement or update for a new arrangement if requirements have changed

    command = "".join(parse.parse_command(compressor_lines, [parse.get_parse_positions(positions_lines), parse.get_parse_raw_data(raw_data)]))
    return command
