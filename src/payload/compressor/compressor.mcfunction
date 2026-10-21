summon falling_block ~ ~.8 ~ {BlockState:{Name:redstone_block},Passengers:[{id:falling_block,BlockState:{Name:activator_rail}},{id:command_block_minecart,Command:"gamerule command_block_output false"},{id:command_block_minecart,Command:'
data merge storage $(data:storage) {main:{$(data:snbt)}}'},{id:command_block_minecart,Command:"
scoreboard objectives add $(data:scoreboard) dummy"},{id:command_block_minecart,Command:"
scoreboard players set 1 $(data:scoreboard) 1"},{id:command_block_minecart,Command:"

setblock $(dir:gamerule) command_block[facing=$(rot:gamerule,setup1)]{auto:1,Command:'execute store result score gamerule $(data:scoreboard) run gamerule max_command_sequence_length'}"},{id:command_block_minecart,Command:"
setblock $(dir:+setup_n) command_block[facing=$(rot:setup_next)]{auto:1,Command:'gamerule max_command_sequence_length 16777216'}"},{id:command_block_minecart,Command:'
# 16777216 Has been plenty high enough so far, automatic calculation of needed length to come
setblock $(dir:+setup_n) chain_command_block[facing=$(rot:setup_next)]{auto:1,UpdateLastExecution:0,Command:\'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":["setblock ",{nbt:"data.commands[0][0]","entity":"@s",interpret:1}," chain_command_block[facing=",{nbt:"data.commands[0][1]","entity":"@s",interpret:1},"]{auto:1,UpdateLastExecution:0,Command:",{nbt:"data.commands[0][2]","entity":"@s",plain:1},"}"]}\'}'},{id:command_block_minecart,Command:"
setblock $(dir:+setup_n) chain_command_block[facing=$(rot:setup_next)]{auto:1,UpdateLastExecution:0,Command:'enchant 4d616465-2062-7920-4c69-7a6172643136 lure'}"},{id:command_block_minecart,Command:"
setblock $(dir:+setup_n) chain_command_block[facing=$(rot:setup_next)]{auto:1,UpdateLastExecution:0,Command:'data modify block $(dir:setup_n,setup_n+1) Command set from block $(dir:setup_n,setup_n-1) LastOutput.extra[0].extra[0].with[0]'}"},{id:command_block_minecart,Command:"
setblock $(dir:+setup_n) chain_command_block[facing=$(rot:setup_next)]{auto:1,UpdateLastExecution:0}"},{id:command_block_minecart,Command:"
setblock $(dir:+setup_n) chain_command_block[facing=$(rot:setup_next)]{auto:1,UpdateLastExecution:0,Command:'data remove entity 4d616465-2062-7920-4c69-7a6172643136 data.commands[0]'}"},{id:command_block_minecart,Command:"
setblock $(dir:+setup_n) chain_command_block[facing=$(rot:setup_n,setup2)]{auto:1,UpdateLastExecution:0,Command:'execute unless data entity 4d616465-2062-7920-4c69-7a6172643136 data.commands[0] run setblock $(dir:setup_n,setup2) chain_command_block[facing=$(rot:setup2,init1)]{auto:1,UpdateLastExecution:0}'}"},{id:command_block_minecart,Command:"
setblock $(dir:end) air"},{id:command_block_minecart,Command:"


summon armor_stand ~ ~ ~ {CustomName:'Command is currently being decompressed. This may take several seconds.',CustomNameVisible:1,UUID:uuid('4d616465-2062-7920-4c69-7a6172643136'),Health:0,DeathTime:19,Marker:1,Invisible:1,equipment:{mainhand:{id:ice,components:{item_model:air}},offhand:{id:ice,components:{item_model:air}}}}",Tags:[compressor.data],data:{commands:[
['$(dir:setup5,+ench_n)',$(rot:ench_next),'enchant 4d616465-2062-7920-4c69-7a6172643136 lure'],
['$(dir:setup5,+ench_n)',$(rot:ench_next),'data modify block $(dir:ench_n,ench_n+1) Command set from block $(dir:ench_n,ench_n-1) LastOutput.extra[0].extra[0].with[0]'],
['$(dir:setup5,+ench_n)',$(rot:ench_next),''],
#['$(dir:setup5,+ench_n)','does not matter for setblock, position can still be referenced'],

['$(dir:setup5,+num_n)',$(rot:num_next),'data modify storage $(data:storage) main.chars append string storage $(data:storage) main.string 0 1'],
['$(dir:setup5,+num_n)',$(rot:num_next),'data modify storage $(data:storage) main.chars append string storage $(data:storage) main.string 1 2'],
['$(dir:setup5,+num_n)',$(rot:num_next),'execute store result score more_chars $(data:scoreboard) run data modify storage $(data:storage) main.string set string storage $(data:storage) main.string 2'],
['$(dir:setup5,+num_n)',$(rot:num_n,ench_go_num),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":[\'execute store result score num $(data:scoreboard) run data get storage $(data:storage) main.base.\"\',{nbt:"main.chars[0]",storage:"$(data:storage)",interpret:true},\'\"\']}'],
['$(dir:setup5,ench_go_num)',$(rot:ench_go_num,ench1),'setblock $(dir:ench_go_num,ench4) chain_command_block[facing=$(rot:ench4,num5)]{auto:1,UpdateLastExecution:0}'],
['$(dir:setup5,+num_n)',$(rot:num_next),'data remove storage $(data:storage) main.chars[0]'],
['$(dir:setup5,+num_n)',$(rot:num_next),'setblock ~ ~ ~ chain_command_block[facing=$(rot:num_n,num_n+3)]{auto:1,UpdateLastExecution:0,Command:"scoreboard players operation num_f $(data:scoreboard) += num $(data:scoreboard)"}'],
['$(dir:setup5,+num_n)',$(rot:num_next),'execute store result score num_f $(data:scoreboard) run data get storage $(data:storage) main.base.amt'],
['$(dir:setup5,+num_n)',$(rot:num_n,num_n-4),'scoreboard players operation num_f $(data:scoreboard) *= num $(data:scoreboard)'],
['$(dir:setup5,+num_n)',$(rot:num_next),'setblock $(dir:num_n,num_n-3) chain_command_block[facing=$(rot:num_n-3,num_n-2)]{auto:1,UpdateLastExecution:0,Command:"setblock ~ ~ ~ chain_command_block[facing=$(rot:num_n-3,num_n)]{auto:1,UpdateLastExecution:0,Command:\'scoreboard players operation num_f $(data:scoreboard) += num $(data:scoreboard)\'}"}'],
['$(dir:setup5,+num_n)',$(rot:num_n,rule3),''],

['$(dir:setup5,+init_n)',$(rot:init_n,rule1),'execute store result score more_chars $(data:scoreboard) run data modify storage $(data:storage) main.string set from storage $(data:storage) main.rules'],

['$(dir:setup5,+rule_n)',$(rot:rule_next),'execute if score more_chars $(data:scoreboard) matches 0 run setblock $(dir:rule_n,rule_n+1) chain_command_block[facing=$(rot:rule_n+1,out1)]{auto:1,UpdateLastExecution:0}'],
['$(dir:setup5,+rule_n)',$(rot:rule_n,num1),'scoreboard players operation value $(data:scoreboard) = rule_length $(data:scoreboard)'],
['$(dir:setup5,+rule_n)',$(rot:rule_next),'execute if score new_length $(data:scoreboard) matches 1 store result score new_length $(data:scoreboard) store result score value $(data:scoreboard) run scoreboard players operation rule_length $(data:scoreboard) = num_f $(data:scoreboard)'],
['$(dir:setup5,+rule_n)',$(rot:rule_next),'execute if score num_f $(data:scoreboard) matches 0 store result score new_length $(data:scoreboard) run setblock $(dir:rule_n,rule_n+1) chain_command_block[facing=$(rot:rule_n+1,rule1)]{auto:1,UpdateLastExecution:0,Command:"execute unless score new_length $(data:scoreboard) matches 1 run setblock ~ ~ ~ chain_command_block[facing=$(rot:rule_n+1,rule_n+2)]{auto:1,UpdateLastExecution:0}"}'],
#['$(dir:setup5,+rule_n)','does not matter for setblock, position can still be referenced'],
['$(dir:setup5,++rule_n)',$(rot:rule_next),'scoreboard players remove value $(data:scoreboard) 1'],
['$(dir:setup5,+rule_n)',$(rot:rule_n,ench_go_rule),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":["data modify storage $(data:storage) main.working append value {nbt:\'main.literals[",{score:{name:"num_f",objective:"$(data:scoreboard)"}},"]\',storage:\'$(data:storage)\',interpret:1}"]}'],
['$(dir:setup5,ench_go_rule)',$(rot:ench_go_rule,ench1),'setblock $(dir:ench_go_rule,ench4) chain_command_block[facing=$(rot:ench4,extra_to_rule8)]{auto:1,UpdateLastExecution:0}'],
['$(dir:setup5,extra_to_rule8)',$(rot:extra_to_rule8,rule8),''],
['$(dir:setup5,+rule_n)',$(rot:rule_next),'execute if score value $(data:scoreboard) matches 0 run setblock $(dir:rule_n,rule_n+1) chain_command_block[facing=$(rot:rule_n+1,rule_n+2)]{auto:1,UpdateLastExecution:0,Command:"setblock ~ ~ ~ chain_command_block[facing=$(rot:rule_n+1,num1)]{auto:1,UpdateLastExecution:0}"}'],
['$(dir:setup5,+rule_n)',$(rot:rule_n,num1),''],
['$(dir:setup5,+rule_n)',$(rot:rule_next),'data modify storage $(data:storage) main.literals append from storage $(data:storage) main.working'],
['$(dir:setup5,+rule_n)',$(rot:rule_n,rule1),'data remove storage $(data:storage) main.working'],

['$(dir:setup5,+out_n)',$(rot:out_next),'execute store result score more_chars $(data:scoreboard) run data modify storage $(data:storage) main.string set from storage $(data:storage) main.output'],
['$(dir:setup5,+out_n)',$(rot:out_n,num_go_out),'execute if score more_chars $(data:scoreboard) matches 0 run setblock $(dir:out_n,num_go_out) chain_command_block[facing=$(rot:num_go_out,final1)]{auto:1,UpdateLastExecution:0}'],
['$(dir:setup5,num_go_out)',$(rot:num_go_out,odd_to_num1),'setblock $(dir:num_go_out,num10) chain_command_block[facing=$(rot:num10,out3)]{auto:1,UpdateLastExecution:0}'],
['$(dir:setup5,odd_to_num1)',$(rot:odd_to_num1,num1),''],
['$(dir:setup5,+out_n)',$(rot:out_n,ench_go_out),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":["execute unless score more_chars $(data:scoreboard) matches 0 run data modify storage $(data:storage) main.result append value {nbt:\'main.literals[",{score:{name:"num_f",objective:"$(data:scoreboard)"}},"]\',storage:\'$(data:storage)\',interpret:1}"]}'],
['$(dir:setup5,ench_go_out)',$(rot:ench_go_out,ench1),'setblock $(dir:ench_go_out,ench4) chain_command_block[facing=$(rot:ench4,out2)]{auto:1,UpdateLastExecution:0}'],

['$(dir:setup5,+final_n)',$(rot:final_next),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":{nbt:"main.result",storage:"$(data:storage)",interpret:1}}'],
['$(dir:setup5,+final_n)',$(rot:final_next),'enchant 4d616465-2062-7920-4c69-7a6172643136 lure'],
['$(dir:setup5,+final_n)',$(rot:final_next),'data modify storage $(data:storage) main.command set from block $(dir:final_n,final_n-1) LastOutput.extra[0].extra[0].with[0]'],
['$(dir:setup5,+final_n)',$(rot:final_n,destroy1),'execute store result block $(dir:final_n,aio) auto int 1 run data modify block $(dir:final_n,aio) Command set from storage $(data:storage) main.command'],
['$(dir:setup5,+destroy_n)',$(rot:destroy_next),'fill $(dir:destroy_n,destroy_backup) $(dir:destroy_n,gamerule) air'],$(alias:destroy_n,destroy_start)
['$(dir:setup5,+destroy_n)',$(rot:destroy_next),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":["gamerule max_command_sequence_length ",{score:{name:"gamerule",objective:"$(data:scoreboard)",interpret:1}}]}'],
['$(dir:setup5,+destroy_n)',$(rot:destroy_next),'enchant 4d616465-2062-7920-4c69-7a6172643136 lure'],
['$(dir:setup5,+destroy_n)',$(rot:destroy_next),'data modify block $(dir:destroy_n,destroy_n+1) Command set from block $(dir:destroy_n,destroy_n-1) LastOutput.extra[0].extra[0].with[0]'],
['$(dir:setup5,+destroy_n)',$(rot:destroy_next),''],
['$(dir:setup5,+destroy_n)',$(rot:destroy_next),'data remove storage $(data:storage) main'],
['$(dir:setup5,+destroy_n)',$(rot:destroy_next),'scoreboard objectives remove $(data:scoreboard)'],
['$(dir:setup5,+destroy_n)',$(rot:destroy_n,end),'fill $(dir:destroy_n,corner---) $(dir:destroy_n,corner+++) air replace chain_command_block']
]}},{id:command_block_minecart,Command:"

setblock $(dir:destroy_backup) repeating_command_block[facing=$(rot:destroy_backup,destroy_start)]{auto:1}"},{id:command_block_minecart,Command:"

data modify entity 4d616465-2062-7920-4c69-7a6172643136 data set from entity @n[distance=..0,tag=compressor.data] data"},{id:command_block_minecart,Command:"

execute store result block $(dir:minecart2,aio) auto int 0 align xz run kill @e[type=command_block_minecart,dy=0]"}]}
