"""
How to structure a command file to use payload features

Uses several custom format implementations in order to automate some otherwise tedious interactions in all in one commands.


Single-line comments can be done in either python (#) or c (//) style
Multi-line commenst can be done in either python (three " or ') or c (/* then */) style
Both comments currenty only support commenting if the comment is at the start of a line.


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

1) $(Name_next) is shorthand for $(Name_n:~:Name_n+1) because it's pretty common to want
    to get the direction of the next in a group and this is more readable.

2) $(Name) Nothing but a name is assumed to be retrieving the position offset from 0 0 0



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

summon falling_block ~ ~.8 ~ {BlockState:{Name:redstone_block},Passengers:[{id:falling_block,BlockState:{Name:activator_rail}},
{id:command_block_minecart,Command:"setblock ~ ~-2 ~ repeating_command_block{auto:1,Command:'fill ~ ~ ~ ~ ~2 ~ air'}"},

{id:command_block_minecart,Command:"say Sample all in one command demonstrating Payload tools"},

"""
Positioning command blocks in sequence

Suppose positions provided in file are as follows:

impulse:(0,1,0)
chain1:(0,2,0)
chain2:(0,3,0)
chain3:(1,3,0)
chain4:(1,2,0)

And suppose these positions were generated with the requirement that chain1 starts next to impulse and chain4 ends next to chain1.

They are then created as such:
$(impulse) retrieves the offset of impulse from 0 0 0
$(impulse:~:chain1) retrieves the facing direction from impulse going to chain1
$(=chain1, first_chain) sets first_chain to mean the first thing as chain_n
    but since chain_n resolves into a dynamic id, it is fixed to whatever the chain sequence was at that time
    in this case, chain1
$(:->:+chain_n) retrieves the offset of chain_n from 0 0 0, specified such that it can originate from somewhere else
    + before chain_n increments the id of chain throughout the command
$(impulse:~:chain_n+1) retrieves the facing direction from impulse going to the next chain, or, +1 in chain's current id
$(+chain_n) does the same thing as $(:->:+chain_n)
$(impulse:~:chain_next) does the same thing as $(impulse:~:chain_n+1)
$(impulse:~:first_chain) retrieves the offset from impulse to first_chain, an alias of chain1
"""
# These command blocks won't do anything and aren't even setup to run multiple times per tick
{id:command_block_minecart,Command:"setblock $(impulse) command_block[facing=$(impulse:~:chain1)]"},
{id:command_block_minecart,Command:"setblock $(+chain_n) chain_command_block[facing=$(chain_n:~:chain_n+1)]"}, $(=chain1,first_chain)
{id:command_block_minecart,Command:"setblock $(+chain_n) chain_command_block[facing=$(chain_n:~:chain_n+1)]"},
{id:command_block_minecart,Command:"setblock $(+chain_n) chain_command_block[facing=$(chain_next)]"},
{id:command_block_minecart,Command:"setblock $(+chain_n) chain_command_block[facing=$(chain_n:~:first_chain)]"},

"""
Inserting raw data somewhere

Suppose you want to insert data generated externally, and suppose that data is as follows:

{"sample_data":"hello world"}

Using it is as such:
$(~sample_data) inserts its value as text (only supports string values)
"""
# Nesting strings isn't handled natively yet, be careful with generating data that may contain more strings for minecraft to interpret
{id:command_block_minecart,Command:"data modify block $(impulse) Command set value '$(~sample_data)'"},

{id:command_block_minecart,Command:"execute align xz run kill @e[type=command_block_minecart,dy=0]"}]}