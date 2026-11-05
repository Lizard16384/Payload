summon falling_block ~ ~.8 ~ {BlockState:{Name:redstone_block},Passengers:[{id:falling_block,BlockState:{Name:activator_rail}},{id:command_block_minecart,Command:"gamerule command_block_output false"},{id:command_block_minecart,Command:'
data merge storage $(data:storage) {main:{$(data:snbt)}}'},{id:command_block_minecart,Command:"
scoreboard objectives add $(data:scoreboard) dummy"},{id:command_block_minecart,Command:"
scoreboard players set 1 $(data:scoreboard) 1"},{id:command_block_minecart,Command:"

setblock $(dir:gamerule) command_block[facing=$(rot:gamerule,setup1)]{auto:1,Command:'execute store result score gamerule $(data:scoreboard) run gamerule max_command_sequence_length'}"},{id:command_block_minecart,Command:"
setblock $(dir:+setup) command_block[facing=$(rot:setup,next)]{auto:1,Command:'gamerule max_command_sequence_length 16777216'}"},{id:command_block_minecart,Command:'
# 16777216 Has been plenty high enough so far, automatic calculation of needed length to come
setblock $(dir:+setup) chain_command_block[facing=$(rot:setup,next)]{auto:1,UpdateLastExecution:0,Command:\'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":["setblock ",{nbt:"data.commands[0][0]","entity":"@s",interpret:1}," chain_command_block[facing=",{nbt:"data.commands[0][1]","entity":"@s",interpret:1},"]{auto:1,UpdateLastExecution:0,Command:",{nbt:"data.commands[0][2]","entity":"@s",plain:1},"}"]}\'}'},{id:command_block_minecart,Command:"
setblock $(dir:+setup) chain_command_block[facing=$(rot:setup,next)]{auto:1,UpdateLastExecution:0,Command:'enchant 4d616465-2062-7920-4c69-7a6172643136 lure'}"},{id:command_block_minecart,Command:"
setblock $(dir:+setup) chain_command_block[facing=$(rot:setup,next)]{auto:1,UpdateLastExecution:0,Command:'data modify block $(dir:setup,next) Command set from block $(dir:setup,prev) LastOutput.extra[0].extra[0].with[0]'}"},{id:command_block_minecart,Command:"
setblock $(dir:+setup) chain_command_block[facing=$(rot:setup,next)]{auto:1,UpdateLastExecution:0}"},{id:command_block_minecart,Command:"
setblock $(dir:+setup) chain_command_block[facing=$(rot:setup,next)]{auto:1,UpdateLastExecution:0,Command:'data remove entity 4d616465-2062-7920-4c69-7a6172643136 data.commands[0]'}"},{id:command_block_minecart,Command:"
setblock $(dir:+setup) chain_command_block[facing=$(rot:setup,setup2)]{auto:1,UpdateLastExecution:0,Command:'execute unless data entity 4d616465-2062-7920-4c69-7a6172643136 data.commands[0] run setblock $(dir:setup,setup2) chain_command_block[facing=$(rot:setup2,init1)]{auto:1,UpdateLastExecution:0}'}"},{id:command_block_minecart,Command:"
setblock $(dir:end) air"},{id:command_block_minecart,Command:"


summon armor_stand ~ ~ ~ {CustomName:'Command is currently being decompressed. This may take several seconds.',CustomNameVisible:1,UUID:uuid('4d616465-2062-7920-4c69-7a6172643136'),Health:0,DeathTime:19,Marker:1,Invisible:1,equipment:{mainhand:{id:ice,components:{item_model:air}},offhand:{id:ice,components:{item_model:air}}}}",Tags:[compressor.data],data:{commands:[
['$(dir:setup5,+ench)',$(rot:ench,next),'enchant 4d616465-2062-7920-4c69-7a6172643136 lure'],
['$(dir:setup5,+ench)',$(rot:ench,next),'data modify block $(dir:ench,next) Command set from block $(dir:ench,prev) LastOutput.extra[0].extra[0].with[0]'],
['$(dir:setup5,+ench)',$(rot:ench,next),''],
#['$(dir:setup5,+ench)','does not matter for setblock, position can still be referenced'],

['$(dir:setup5,+num)',$(rot:num,next),'data modify storage $(data:storage) main.chars append string storage $(data:storage) main.string 0 1'],
['$(dir:setup5,+num)',$(rot:num,next),'data modify storage $(data:storage) main.chars append string storage $(data:storage) main.string 1 2'],
['$(dir:setup5,+num)',$(rot:num,next),'execute store result score more_chars $(data:scoreboard) run data modify storage $(data:storage) main.string set string storage $(data:storage) main.string 2'],
['$(dir:setup5,+num)',$(rot:num,ench_go_num),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":[\'execute store result score num $(data:scoreboard) run data get storage $(data:storage) main.base.\"\',{nbt:"main.chars[0]",storage:"$(data:storage)",interpret:true},\'\"\']}'],
['$(dir:setup5,ench_go_num)',$(rot:ench_go_num,ench1),'setblock $(dir:ench_go_num,ench4) chain_command_block[facing=$(rot:ench4,num5)]{auto:1,UpdateLastExecution:0}'],
['$(dir:setup5,+num)',$(rot:num,next),'data remove storage $(data:storage) main.chars[0]'],
['$(dir:setup5,+num)',$(rot:num,next),'setblock ~ ~ ~ chain_command_block[facing=$(rot:num,num+3)]{auto:1,UpdateLastExecution:0,Command:"scoreboard players operation num_f $(data:scoreboard) += num $(data:scoreboard)"}'],
['$(dir:setup5,+num)',$(rot:num,next),'execute store result score num_f $(data:scoreboard) run data get storage $(data:storage) main.base.amt'],
['$(dir:setup5,+num)',$(rot:num,num-4),'scoreboard players operation num_f $(data:scoreboard) *= num $(data:scoreboard)'],
['$(dir:setup5,+num)',$(rot:num,next),'setblock $(dir:num,num-3) chain_command_block[facing=$(rot:num-3,num-2)]{auto:1,UpdateLastExecution:0,Command:"setblock ~ ~ ~ chain_command_block[facing=$(rot:num-3,num)]{auto:1,UpdateLastExecution:0,Command:\'scoreboard players operation num_f $(data:scoreboard) += num $(data:scoreboard)\'}"}'],
['$(dir:setup5,+num)',$(rot:num,rule3),''],

['$(dir:setup5,+init)',$(rot:init,rule1),'execute store result score more_chars $(data:scoreboard) run data modify storage $(data:storage) main.string set from storage $(data:storage) main.rules'],

['$(dir:setup5,+rule)',$(rot:rule,next),'execute if score more_chars $(data:scoreboard) matches 0 run setblock $(dir:rule,next) chain_command_block[facing=$(rot:latest,out1)]{auto:1,UpdateLastExecution:0}'],
['$(dir:setup5,+rule)',$(rot:rule,num1),'scoreboard players operation value $(data:scoreboard) = rule_length $(data:scoreboard)'],
['$(dir:setup5,+rule)',$(rot:rule,next),'execute if score new_length $(data:scoreboard) matches 1 store result score new_length $(data:scoreboard) store result score value $(data:scoreboard) run scoreboard players operation rule_length $(data:scoreboard) = num_f $(data:scoreboard)'],
['$(dir:setup5,+rule)',$(rot:rule,next),'execute if score num_f $(data:scoreboard) matches 0 store result score new_length $(data:scoreboard) run setblock $(dir:rule,next) chain_command_block[facing=$(rot:latest,rule1)]{auto:1,UpdateLastExecution:0,Command:"execute unless score new_length $(data:scoreboard) matches 1 run setblock ~ ~ ~ chain_command_block[facing=$(rot:rule+1,next)]{auto:1,UpdateLastExecution:0}"}'],
#['$(dir:setup5,+rule)','does not matter for setblock, position can still be referenced'],
['$(dir:setup5,2+rule)',$(rot:rule,next),'scoreboard players remove value $(data:scoreboard) 1'],
['$(dir:setup5,+rule)',$(rot:rule,ench_go_rule),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":["data modify storage $(data:storage) main.working append value {nbt:\'main.literals[",{score:{name:"num_f",objective:"$(data:scoreboard)"}},"]\',storage:\'$(data:storage)\',interpret:1}"]}'],
['$(dir:setup5,ench_go_rule)',$(rot:ench_go_rule,ench1),'setblock $(dir:ench_go_rule,ench4) chain_command_block[facing=$(rot:ench4,extra_to_rule8)]{auto:1,UpdateLastExecution:0}'],
['$(dir:setup5,extra_to_rule8)',$(rot:extra_to_rule8,rule8),''],
['$(dir:setup5,+rule)',$(rot:rule,next),'execute if score value $(data:scoreboard) matches 0 run setblock $(dir:rule,next) chain_command_block[facing=$(rot:latest,next)]{auto:1,UpdateLastExecution:0,Command:"setblock ~ ~ ~ chain_command_block[facing=$(rot:prev,num1)]{auto:1,UpdateLastExecution:0}"}'],
['$(dir:setup5,+rule)',$(rot:rule,num1),''],
['$(dir:setup5,+rule)',$(rot:rule,next),'data modify storage $(data:storage) main.literals append from storage $(data:storage) main.working'],
['$(dir:setup5,+rule)',$(rot:rule,rule1),'data remove storage $(data:storage) main.working'],

['$(dir:setup5,+out)',$(rot:out,next),'execute store result score more_chars $(data:scoreboard) run data modify storage $(data:storage) main.string set from storage $(data:storage) main.output'],
['$(dir:setup5,+out)',$(rot:out,num_go_out),'execute if score more_chars $(data:scoreboard) matches 0 run setblock $(dir:out,num_go_out) chain_command_block[facing=$(rot:num_go_out,final1)]{auto:1,UpdateLastExecution:0}'],
['$(dir:setup5,num_go_out)',$(rot:num_go_out,odd_to_num1),'setblock $(dir:num_go_out,num10) chain_command_block[facing=$(rot:num10,out3)]{auto:1,UpdateLastExecution:0}'],
['$(dir:setup5,odd_to_num1)',$(rot:odd_to_num1,num1),''],
['$(dir:setup5,+out)',$(rot:out,ench_go_out),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":["execute unless score more_chars $(data:scoreboard) matches 0 run data modify storage $(data:storage) main.result append value {nbt:\'main.literals[",{score:{name:"num_f",objective:"$(data:scoreboard)"}},"]\',storage:\'$(data:storage)\',interpret:1}"]}'],
['$(dir:setup5,ench_go_out)',$(rot:ench_go_out,ench1),'setblock $(dir:ench_go_out,ench4) chain_command_block[facing=$(rot:ench4,out2)]{auto:1,UpdateLastExecution:0}'],

['$(dir:setup5,+final)',$(rot:final,next),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":{nbt:"main.result",storage:"$(data:storage)",interpret:1}}'],
['$(dir:setup5,+final)',$(rot:final,next),'enchant 4d616465-2062-7920-4c69-7a6172643136 lure'],
['$(dir:setup5,+final)',$(rot:final,next),'data modify storage $(data:storage) main.command set from block $(dir:final,prev) LastOutput.extra[0].extra[0].with[0]'],
['$(dir:setup5,+final)',$(rot:final,destroy1),'execute store result block $(dir:final,aio) auto int 1 run data modify block $(dir:final,aio) Command set from storage $(data:storage) main.command'],
['$(dir:setup5,+destroy)',$(rot:destroy,next),'fill $(dir:destroy,destroy_backup) $(dir:destroy,gamerule) air'],$(alias:destroy,destroy_start)
['$(dir:setup5,+destroy)',$(rot:destroy,next),'execute as 4d616465-2062-7920-4c69-7a6172643136 run item modify entity @s weapon.mainhand {"function":"minecraft:set_name","entity":"this","name":["gamerule max_command_sequence_length ",{score:{name:"gamerule",objective:"$(data:scoreboard)",interpret:1}}]}'],
['$(dir:setup5,+destroy)',$(rot:destroy,next),'enchant 4d616465-2062-7920-4c69-7a6172643136 lure'],
['$(dir:setup5,+destroy)',$(rot:destroy,next),'data modify block $(dir:destroy,next) Command set from block $(dir:destroy,prev) LastOutput.extra[0].extra[0].with[0]'],
['$(dir:setup5,+destroy)',$(rot:destroy,next),''],
['$(dir:setup5,+destroy)',$(rot:destroy,next),'data remove storage $(data:storage) main'],
['$(dir:setup5,+destroy)',$(rot:destroy,next),'scoreboard objectives remove $(data:scoreboard)'],
['$(dir:setup5,+destroy)',$(rot:destroy,end),'fill $(dir:destroy,_---_) $(dir:destroy,_+++_) air replace chain_command_block']
]}},{id:command_block_minecart,Command:"

setblock $(dir:destroy_backup) repeating_command_block[facing=$(rot:destroy_backup,destroy_start)]{auto:1}"},{id:command_block_minecart,Command:"

data modify entity 4d616465-2062-7920-4c69-7a6172643136 data set from entity @n[distance=..0,tag=compressor.data] data"},{id:command_block_minecart,Command:"

execute store result block $(dir:minecart2,aio) auto int 0 align xz run kill @e[type=command_block_minecart,dy=0]"}]}
