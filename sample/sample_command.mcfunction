summon falling_block ~ ~.8 ~ {BlockState:{Name:redstone_block},Passengers:[{id:falling_block,BlockState:{Name:activator_rail}},
{id:command_block_minecart,Command:"setblock ~ ~-2 ~ repeating_command_block{auto:1,Command:'fill ~ ~ ~ ~ ~2 ~ air'}"},

{id:command_block_minecart,Command:"say Sample all in one command demonstrating Payload tools"},

# The following command blocks won't do anything and aren't even setup to run multiple times per tick
# See sample_position_requirements.py for an example of how these positions were generated

{id:command_block_minecart,Command:"setblock $(dir:impulse) command_block[facing=$(rot:impulse,chain1)]"},
{id:command_block_minecart,Command:"setblock $(dir:+chain) chain_command_block[facing=$(rot:chain,chain+1)]"}, $(alias:chain1,first_chain)
{id:command_block_minecart,Command:"setblock $(dir:+chain) chain_command_block[facing=$(rot:chain,chain+1)]"},
{id:command_block_minecart,Command:"setblock $(dir:+chain) chain_command_block[facing=$(rot:chain_next)]"},
{id:command_block_minecart,Command:"setblock $(dir:+chain) chain_command_block[facing=$(rot:chain,first_chain)]"},
{id:command_block_minecart,Command:"data modify block $(dir:impulse) Command set value '$(data:sample_data)'"},
# Custom data insertion can be generated however as long as it is externally provided as a dictionary with string keys and values.

{id:command_block_minecart,Command:"execute align xz run kill @e[type=command_block_minecart,dy=0]"}]}
