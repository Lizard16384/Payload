# Payload

A tool for creating All In One Commands in modern versions of Minecraft by greatly increasing the usable length of a command.

# How to use

Payload's tools are designed to be used with raw text. You can choose what to do by providing different text files that designate how to interact with whatever it is you're trying to do.

## Compressing

\* After all other automations have been done and you have a too long, but otherwise completely valid, command:

Call final() with the command string, the mode(s) of output (options are "clipboard" and/or "write), and optionally the file to write to if outputting a file (default is "result.txt)

# Functional Overview

## Why it works

If you've worked with all in one commands before, chances are you know that Minecraft will not let you run a command longer than 32,500 characters in length. Or rather, that's the oversimplication you may know. What's actually happening is that Minecraft has a limit on the length of a string that can be sent to the server or received by the client of, in most cases, about that long. Thus, the limit of a command block is artificially imposed to prevent you from pasting more than 32,500 characters into its menu.

But there is no limit to the length of a command that can be run by the server. Good luck getting it there, but then it works just fine; that's what Payload does.

## Compression

The most important aspect of this project is what gets it useful in the first place: the compression, which I have named the Payload. Outside of the context of Minecraft, all that is being done is lossless data compression. I have chosen to base the compression on the [Re-Pair algorithm](https://en.wikipedia.org/wiki/Re-Pair). To keep it short; you take a sequence of values, say integers, find the most common occurence of two of the same values next to each other, and then replace it for a new value while defining somewhere else that you replaced those two values for one value. Now you only have to specify the two values together once, plus its new value, and then the new value everywhere it occured, as opposed to always having to specify the two values together. For large occurences, it might as well half the data required to represent those two values.

For example, say you have the string "abc abc abc defg". The pairing "ab" occurs most frequently, so you replace the string to be something like "Xc Xc Xcdefg", and you track that "X" = "ab". Now the pair "Xc" occurs most freqently, the string turns into "Y Y Ydefg" and "Y" = "Xc". Once more turns into "ZZZdefg" with "Z" = "Y ".

Do this over and over again, and pretty quickly you have a much more efficient way of representing the same data. One of the primary reasons I like this algorithm is because most of its complication happens during encoding, while its decoding sequence is incredibly straight forward and easy to work with: take a value, substitute it for that value's definition of other values, repeat until finished. This is useful because I want to use as little logic as possible to decode once in Minecraft: uncompressed characters are a lot more costly to what can be fit in the command than whatever's going on inside the payload.

Beyond re-pair, there are a few more things done before considering the compressed data complete. Most importantly, pair replacements are condensed when two pairs are only ever used together. For example, in the string "abc abc abc abc", "ab" and "bc" are only ever seen in "abc", so instead of having replacements turn "ab" into "X" and "Xc" into "Y", it can go straight from "abc" to "Y". This comes with the downside of variable-length replacements and you can no longer assume everything just replaces two values together. This is almost entirely inconsequential to both the command blocks required to interpret it and the data itself by sorting the replacements by ascending length and reserving a value that says "hey you're about to change the replacement length" followed by the new length, and then resume the replacements with the new length of each one.

Lastly, with lots of compressed data, it needs to be optimized to send the data in a command. The current method of doing this is to convert each number into the highest needed base (up to 92) depending on how many unique values there are, and use two characters to represent each value. This isn't as efficient as it can be yet, future versions may work differently.

## Enchant Flattening

The reason Payload, and a lot of other things I do with commands, is possible is thanks to an incredibly obscure trick known as enchant flattening. I have not been able to find any documentation for it that is relevant for how I use it in modern versions. It probably has something to do with the fact that it is not guaranteed behavior and may be modified or removed at any time as I do not think it is technically a feature, but it's been strong going since 1.19ish, with its only severe limitation being removed in 1.20.5 with the change of text components into snbt. Considering it's the only way (that I know of) to flatten text components, and thus assemble strings to be parsed as commands, I'm happy to rely on it due to the incredible amount of power it provides.

Nuances aside, all that's happening is that the chat output when an enchant command fails will flatten text components from anything into one string of rawtext of whatever that text component was representing, turning ["say ","test"], which is unusable as a command, into "say test", which can be set and parsed as a command. What little documentation of enchant flattening exists, and that is outdated, will explain that you set a sign to have text components such as nbt and score that need to be [resolved](https://minecraft.wiki/w/Text_component_format#Component_resolution), then set an entity such as an armor stand to have the sign's resulting text as a custom name, then run /enchant on the entity, then make use of the string located at data extra[0].extra[0].with[0] in the command block that ran enchant as one full string with dynamically assembled values. Essentially, it's a function macro command without a datapack. However, I prefer using an item modifier to an armor stand holding an item to set the item's custom name which combines the steps of the sign and the custom name by the fact that item modifiers can resolve text components and item name shows up in the enchant fail output in one step instead of two and one less sign needed. I have yet to see that done anywhere else.

# Why are you still working with all in one commands

"It's 2026 bro we have datapacks"

I've heavily prioritized my values around quick and easy. Especially in the context of my first project, chess, I'm not in it for the chess. If I was in it for the chess then I'd send you to one of the many preexisting chess datapacks. I'm in it for the unique fun and novelty of an all in one command; a quick little thing that requires exactly zero setup. Plus it's fun to optimize things in ways you never would with datapacks, which leads to these things like Payload that significantly improve development.

While it's possible to just split a long command into multiple commands and have the player copy/paste multiple commands, that harms ease of use and ease of development. Payload makes it so that you only have to copy and paste a single command, and the time that you may have spent copying and pasting multiple commands and following the creator-defined instructions on how to do so is instead spent letting it do its thing. Splitting it into multiple commands has the obvious drawback that means I would have to split it into multiple commands. That's how it was done before I created Payload, and while it worked, I was constantly thinking about how close to the character limit I was and what things I could optimize to be able to fit in more stuff in however many command blocks I already allocated to the project. However, "just use another command block" was never really the solution for me because it made it more annoying to use and harder to create. Payload solves a lot of problems at once: I don't have to deal with multiple commands at once and how they should integrate, I effectively don't have to worry about the length of my command being an issue for making it possible to use, and it wraps everything into an external script which allows for things like comments and automatic text replacement for whatever processes I want to make smoother.
