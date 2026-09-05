#!/usr/bin/env python3
"""Using Payload

"""
from pathlib import Path

from payload.parser import parse
from payload import finish
from payload.positioner import calculate_positions

import sample_position_requirements

def main():
    # Basics of making use of the main features of payload - compressing, position replacement, and raw data insertion
    command_path = Path("sample_command.mcfunction")  # Base command to compress, formatted to be used with various tools
    positions_path = Path("sample_positions.txt")  # Positions generated if using the bruteforce position calculator - autogenerates and updates, but needs file name provided
    some_other_raw_data = {"sample_data":"hello world"}  # Misc key/value data that can be sourced however to insert stuff not natively calculated
    command_lines = finish.read_file_lines(command_path)  # Format command by lines to give to parser
    requirements = sample_position_requirements.return_data()  # Data for the bruteforce positioning, verified at each run but only recalculated when setup no longer fits
    positions_lines = calculate_positions.calculate(requirements, positions_path)  # Bruteforce position calculation - either creates a new layout or uses preexisting (if valid) layout
    final_command_lines = parse.parse_command(command_lines, [parse.get_parse_positions(positions_lines), parse.get_parse_raw_data(some_other_raw_data)])  # Parse all data into command
    finish.finish("".join(final_command_lines), ("clipboard","write"), "sample_payload.txt")  # Compress command and run end behavior
    # Note that the final command is separated by lines before being given to the compressor - behavior subject to change but exists for a reason

if __name__ == "__main__":
    main()
