summon falling_block ~ ~.8 ~ {BlockState:{Name:redstone_block},Passengers:[{id:falling_block,BlockState:{Name:activator_rail}},{id:command_block_minecart,Command:"gamerule command_block_output false"},{id:command_block_minecart,Command:'
data merge storage $(~storage) {main:{$(~snbt)}}'},{id:command_block_minecart,Command:"
scoreboard objectives add $(~scoreboard) dummy"},{id:command_block_minecart,Command:"
scoreboard players set 1 $(~scoreboard) 1"},{id:command_block_minecart,Command:"

setblock $(+setup_n) command_block[facing=$(setup_next)]{auto:1,Command:'setblock ~ ~ ~ air'}"},{id:command_block_minecart,Command:'
setblock $(+setup_n) chain_command_block[facing=$(setup_next)]{auto:1,UpdateLastExecution:0,Command:\'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":["setblock ",{nbt:"data.commands[0][0]","entity":"@s",interpret:1}," chain_command_block[facing=",{nbt:"data.commands[0][1]","entity":"@s",interpret:1},"]{auto:1,UpdateLastExecution:0,Command:",{nbt:"data.commands[0][2]","entity":"@s",plain:1},"}"]}\'}'},{id:command_block_minecart,Command:"
setblock $(+setup_n) chain_command_block[facing=$(setup_next)]{auto:1,UpdateLastExecution:0,Command:'enchant 4d616465-2062-7920-4c69-7a6172643136 lure'}"},{id:command_block_minecart,Command:"
setblock $(+setup_n) chain_command_block[facing=$(setup_next)]{auto:1,UpdateLastExecution:0,Command:'data modify block $(setup_n:->:setup_n+1) Command set from block $(setup_n:->:setup_n-1) LastOutput.extra[0].extra[0].with[0]'}"},{id:command_block_minecart,Command:"
setblock $(+setup_n) chain_command_block[facing=$(setup_next)]{auto:1,UpdateLastExecution:0}"},{id:command_block_minecart,Command:"
setblock $(+setup_n) chain_command_block[facing=$(setup_next)]{auto:1,UpdateLastExecution:0,Command:'data remove entity 4d616465-2062-7920-4c69-7a6172643136 data.commands[0]'}"},{id:command_block_minecart,Command:"
setblock $(+setup_n) chain_command_block[facing=$(setup_n:~:setup2)]{auto:1,UpdateLastExecution:0,Command:'execute unless data entity 4d616465-2062-7920-4c69-7a6172643136 data.commands[0] run setblock $(setup_n:->:setup2) chain_command_block[facing=$(setup2:~:init1)]{auto:1,UpdateLastExecution:0}'}"},{id:command_block_minecart,Command:"
setblock $(end) air"},{id:command_block_minecart,Command:"

summon armor_stand ~ ~ ~ {UUID:uuid('4d616465-2062-7920-4c69-7a6172643136'),Health:0,DeathTime:19,Marker:1,Invisible:1,equipment:{mainhand:{id:ice,components:{item_model:air}},offhand:{id:ice,components:{item_model:air}}}}",Tags:[compressor.data],data:{commands:[

['$(setup5:->:+ench_n)',$(ench_next),'enchant 4d616465-2062-7920-4c69-7a6172643136 lure'],
['$(setup5:->:+ench_n)',$(ench_next),'data modify block $(ench_n:->:ench_n+1) Command set from block $(ench_n:->:ench_n-1) LastOutput.extra[0].extra[0].with[0]'],
['$(setup5:->:+ench_n)',$(ench_next),''],
#['$(setup5:->:+ench_n)','does not matter for setblock, position can still be referenced'],

['$(setup5:->:+num_n)',$(num_next),'data modify storage $(~storage) main.chars append string storage $(~storage) main.string 0 1'],
['$(setup5:->:+num_n)',$(num_next),'data modify storage $(~storage) main.chars append string storage $(~storage) main.string 1 2'],
['$(setup5:->:+num_n)',$(num_next),'execute store result score more_chars $(~scoreboard) run data modify storage $(~storage) main.string set string storage $(~storage) main.string 2'],
['$(setup5:->:+num_n)',$(num_n:~:ench_go_num),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":[\'execute store result score num $(~scoreboard) run data get storage $(~storage) main.base.\"\',{nbt:"main.chars[0]",storage:"$(~storage)",interpret:true},\'\"\']}'],
['$(setup5:->:ench_go_num)',$(ench_go_num:~:ench1),'setblock $(ench_go_num:->:ench4) chain_command_block[facing=$(ench4:~:num5)]{auto:1,UpdateLastExecution:0}'],
['$(setup5:->:+num_n)',$(num_next),'data remove storage $(~storage) main.chars[0]'],
['$(setup5:->:+num_n)',$(num_next),'setblock ~ ~ ~ chain_command_block[facing=$(num_n:~:num_n+3)]{auto:1,UpdateLastExecution:0,Command:"scoreboard players operation num_f $(~scoreboard) += num $(~scoreboard)"}'],
['$(setup5:->:+num_n)',$(num_next),'execute store result score num_f $(~scoreboard) run data get storage $(~storage) main.base.amt'],
['$(setup5:->:+num_n)',$(num_n:~:num_n-4),'scoreboard players operation num_f $(~scoreboard) *= num $(~scoreboard)'],
['$(setup5:->:+num_n)',$(num_next),'setblock $(num_n:->:num_n-3) chain_command_block[facing=$(num_n-3:~:num_n-2)]{auto:1,UpdateLastExecution:0,Command:"setblock ~ ~ ~ chain_command_block[facing=$(num_n-3:~:num_n)]{auto:1,UpdateLastExecution:0,Command:\'scoreboard players operation num_f $(~scoreboard) += num $(~scoreboard)\'}"}'],
['$(setup5:->:+num_n)',$(num_n:~:rule3),''],

['$(setup5:->:+init_n)',$(init_n:~:rule1),'execute store result score more_chars $(~scoreboard) run data modify storage $(~storage) main.string set from storage $(~storage) main.rules'],

['$(setup5:->:+rule_n)',$(rule_next),'execute if score more_chars $(~scoreboard) matches 0 run setblock $(rule_n:->:rule_n+1) chain_command_block[facing=$(rule_n+1:~:out1)]{auto:1,UpdateLastExecution:0}'],
['$(setup5:->:+rule_n)',$(rule_n:~:num1),'scoreboard players operation value $(~scoreboard) = rule_length $(~scoreboard)'],
['$(setup5:->:+rule_n)',$(rule_next),'execute if score new_length $(~scoreboard) matches 1 store result score new_length $(~scoreboard) store result score value $(~scoreboard) run scoreboard players operation rule_length $(~scoreboard) = num_f $(~scoreboard)'],
['$(setup5:->:+rule_n)',$(rule_next),'execute if score num_f $(~scoreboard) matches 0 store result score new_length $(~scoreboard) run setblock $(rule_n:->:rule_n+1) chain_command_block[facing=$(rule_n+1:~:rule1)]{auto:1,UpdateLastExecution:0,Command:"execute unless score new_length $(~scoreboard) matches 1 run setblock ~ ~ ~ chain_command_block[facing=$(rule_n+1:~:rule_n+2)]{auto:1,UpdateLastExecution:0}"}'],
#['$(setup5:->:+rule_n)','does not matter for setblock, position can still be referenced'],
['$(setup5:->:++rule_n)',$(rule_next),'scoreboard players remove value $(~scoreboard) 1'],
['$(setup5:->:+rule_n)',$(rule_n:~:ench_go_rule),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":["data modify storage $(~storage) main.working append value {nbt:\'main.literals[",{score:{name:"num_f",objective:"$(~scoreboard)"}},"]\',storage:\'$(~storage)\',interpret:1}"]}'],
['$(setup5:->:ench_go_rule)',$(ench_go_rule:~:ench1),'setblock $(ench_go_rule:->:ench4) chain_command_block[facing=$(ench4:~:extra_to_rule8)]{auto:1,UpdateLastExecution:0}'],
['$(setup5:->:extra_to_rule8)',$(extra_to_rule8:~:rule8),''],
['$(setup5:->:+rule_n)',$(rule_next),'execute if score value $(~scoreboard) matches 0 run setblock $(rule_n:->:rule_n+1) chain_command_block[facing=$(rule_n+1:~:rule_n+2)]{auto:1,UpdateLastExecution:0,Command:"setblock ~ ~ ~ chain_command_block[facing=$(rule_n+1:~:num1)]{auto:1,UpdateLastExecution:0}"}'],
['$(setup5:->:+rule_n)',$(rule_n:~:num1),''],
['$(setup5:->:+rule_n)',$(rule_next),'data modify storage $(~storage) main.literals append from storage $(~storage) main.working'],
['$(setup5:->:+rule_n)',$(rule_n:~:rule1),'data remove storage $(~storage) main.working'],

['$(setup5:->:+out_n)',$(out_next),'execute store result score more_chars $(~scoreboard) run data modify storage $(~storage) main.string set from storage $(~storage) main.output'],
['$(setup5:->:+out_n)',$(out_n:~:num_go_out),'execute if score more_chars $(~scoreboard) matches 0 run setblock $(out_n:->:num_go_out) chain_command_block[facing=$(num_go_out:~:final1)]{auto:1,UpdateLastExecution:0}'],
['$(setup5:->:num_go_out)',$(num_go_out:~:odd_to_num1),'setblock $(num_go_out:->:num10) chain_command_block[facing=$(num10:~:out3)]{auto:1,UpdateLastExecution:0}'],
['$(setup5:->:odd_to_num1)',$(odd_to_num1:~:num1),''],
['$(setup5:->:+out_n)',$(out_n:~:ench_go_out),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":["execute unless score more_chars $(~scoreboard) matches 0 run data modify storage $(~storage) main.result append value {nbt:\'main.literals[",{score:{name:"num_f",objective:"$(~scoreboard)"}},"]\',storage:\'$(~storage)\',interpret:1}"]}'],
['$(setup5:->:ench_go_out)',$(ench_go_out:~:ench1),'setblock $(ench_go_out:->:ench4) chain_command_block[facing=$(ench4:~:out2)]{auto:1,UpdateLastExecution:0}'],

['$(setup5:->:+final_n)',$(final_next),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":{nbt:"main.result",storage:"$(~storage)",interpret:1}}'],
['$(setup5:->:+final_n)',$(final_next),'enchant 4d616465-2062-7920-4c69-7a6172643136 lure'],
['$(setup5:->:+final_n)',$(final_next),'data modify storage $(~storage) main.command set from block $(final_n:->:final_n-1) LastOutput.extra[0].extra[0].with[0]'],
['$(setup5:->:+final_n)',$(final_next),'execute store result block $(final_n:->:aio) auto int 1 run data modify block $(final_n:->:aio) Command set from storage $(~storage) main.command'],
['$(setup5:->:+final_n)',$(final_next),'data remove storage $(~storage) main'],$(=final_n,destroy_start)
['$(setup5:->:+final_n)',$(final_next),'scoreboard objectives remove $(~scoreboard)'],
['$(setup5:->:+final_n)',$(final_next),'kill @n[tag=compressor.text]'],
['$(setup5:->:+final_n)',$(final_n:~:end),'fill $(final_n:->:corner---) $(final_n:->:corner+++) air replace chain_command_block']
]}},{id:command_block_minecart,Command:"

setblock $(destroy_backup) repeating_command_block[facing=$(destroy_backup:~:destroy_start)]{auto:1,Command:'setblock ~ ~ ~ air'}"},{id:command_block_minecart,Command:"

data modify entity 4d616465-2062-7920-4c69-7a6172643136 data set from entity @n[distance=..0,tag=compressor.data] data"},{id:command_block_minecart,Command:"

summon text_display ~ ~ ~ {Tags:[compressor.text],billboard:vertical,line_width:999,text:'Thank you for using Payload by Lizard16!\n\nCommand is currently being decompressed.\nThis may take several seconds.'}"},{id:command_block_minecart,Command:"

execute store result block $(minecart2:->:aio) auto int 0 align xz run kill @e[type=command_block_minecart,dy=0]"}]}
