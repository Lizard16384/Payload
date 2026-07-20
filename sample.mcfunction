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
$(~<key>) inserts its value as text (only supports string values)
"""
# Nesting strings isn't handled natively yet, be careful with generating data that may contain more strings for minecraft to interpret
{id:command_block_minecart,Command:"data modify block $(impulse) Command set value '$(~sample_data)'"},

{id:command_block_minecart,Command:"execute align xz run kill @e[type=command_block_minecart,dy=0]"}]}