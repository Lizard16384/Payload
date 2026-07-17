# Do not edit these
from payload.parser import parse
from payload.compressor import compress
from payload import finish

def main():
    # Parsing a command is assumed to have a raw command file, a file specifying names of positions and their given coordinates to insert where specified in the raw command, and optional misc data.
    in_command = "path_to_raw_command"
    in_positions = "path_to_command_block_positions"
    some_other_parsing_data = {}
    command = parse.parse_command(finish.read_file_lines(in_command),finish.read_file_lines(in_positions),some_other_parsing_data)

    # command no longer has any data to be inserted and is ready to be compressed. Optionally you can rename the storage and scoreboard used by the compressor.
    raw_data = {"storage":"c","scoreboard":"c"}
    final_command = compress.compile_command(command, raw_data)
    finish.finish(final_command, ("clipboard","write"), "result.txt")

if __name__ == "__main__":
    main()
