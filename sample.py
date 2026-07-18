"""How to structure a command file to use payload features

Uses several custom format implementations in order to automate some otherwise tedious interactions in all in one commands.

Custom actions are embedded in a $(), unless the string "$(" is required unaffected for some reason, in which case escaping it with a backslash will ignore it.
This is the same way datapack function macros handle runtime data insertion. After the fact, payload requires formatting to specify what to do with it



How position data is handled and used

* Give the parser a list of each name and its coordinate with parse.get_parse_positions(positions_lines) in parse.parse_command()
* Each line is formatted "<name>:(<x>,<y>,<z>)"

Automating position placement by fixing the coordinate of the position
somewhere other than where it is used allows for not caring where anything is
located relative to each other in development, which eliminates needing to go
through commands and update relative coordinates every time something changes.

Names are given to relative coordinate offsets specified in a file or generated
elsewhere to be inserted and interpreted as needed.
1) _n
    Any time a name ends in _n, it is dynamtically incrementing. Every time
    the entire name is prepended with a "+", that increments the current _n id and then
    uses that value there, i.e. "+A_n" behaves the same as referring to "A_n" while
    also incrementing the id. Any time the entire name is appended with "+<#>" or "-<#>",
    it refers to that many positions back in the _n sequence, i.e. "A_n+1"

    So the sequence $(+A_n) $(+A_n) $(+A_n) is treated the same as
    the sequence $(+A1) $(+A2) $(+A3) and refers to those position names by
    incrementing gradually throughout the file.

2) $(=Name,Name2)
    Adds an alias to Name2. This is particularly useful for adding an alias to
    an _n name, as those are changing as the file is read and you may want
    to refer to one particular block no matter what its processed _n value is.
    This does not insert any data into the command.

3) $(Name1:->:Name2) Gets the local coordinate change from 1 to 2 and inserts as a relative offset
    3b) If either 1 or 2 is empty, it is treated as 0 0 0

4) $(Name1:~:Name2) Gets the direction N/S/E/W/U/D going from 1 to 2 and inserts for block state use
    Only intended if the two coordinates are next to each other: it is already
    assumed that they are next to each other when doing this.

Shorthand syntax to do same things mentioned above:

1) $(Name__next) is shorthand for $(Name_n:~:Name_n+1) because it's pretty common to want
    to get the direction of the next in a group and this is more readable.

2) $(Name) Nothing but a name is assumed to be retrieving the position, or, the same as $(:->:Name)



How raw data is handled and used

* Raw data is given as a dictionary with parse.get_parse_raw_data(positions_lines) in parse.parse_command()

Raw data in a command is defined using $(~<key>) and will insert the string value there in the command.
    Does not support anything other than strings as values as the command is always a string.
    Does not yet support defining a path in the dictionary beyond surface-level string values.



How to calculate positional requirements

At the moment, this feature is not integrated to be properly usable.
Will get back to it after stable releases.



At the moment, this is all that the parser does, whist being the medium with which to make use of compression.
"""

from payload.parser import parse
from payload import finish

def main():
    # Basics of making use of the main features of payload - compressing, position replacement, and raw data insertion
    in_command = "path_to_raw_command/command.txt"
    in_positions = "path_to_command_block_positions/positions.txt"
    some_other_raw_data = {}
    command_lines = finish.read_file_lines(in_command)
    positions_lines = finish.read_file_lines(in_positions)
    final_command = parse.parse_command(command_lines, [parse.get_parse_positions(positions_lines), parse.get_parse_raw_data(some_other_raw_data)])
    finish.finish(final_command, ("clipboard","write"), "result.txt")

if __name__ == "__main__":
    main()
