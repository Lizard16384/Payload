# Do not edit these
from payload.parser import parse
from payload import finish
from importlib import resources

def main():
    in_command = "path_to_raw_command"
    in_positions = "path_to_command_block_positions"
    some_other_raw_data = {}
    command_lines = finish.read_file_lines(in_command)
    positions_lines = finish.read_file_lines(in_positions)
    final_command = parse.parse_command(command_lines, [parse.get_parse_positions(positions_lines), parse.get_parse_raw_data(some_other_raw_data)])
    finish.finish(final_command, ("clipboard","write"), "result.txt")

if __name__ == "__main__":
    main()
