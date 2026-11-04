# Payload Inline Format

Uses custom format implementations in order to automate some otherwise tedious processes. The idea behind such automation is for ease of development while still allowing full control of the result.

> **Note:** Payload is not a typical all-in-one command "generator" in the sense that you have several commands and you just want to throw them together and assume they all get run when you paste a large generated result. Payload is assumed to be working with one, complete, valid, all in one command, and provides tools to aid development of that command; primarily by providing a means to run commands longer than the standard command block length limit. This file documents how to use the rest of Payload's functionality.

## Core Grammar

`$(tag:body)`

Payload generally interacts with a command by providing inline calls for custom actions alongside necessary information about how those actions are to be interpreted.

Every action is a `tag` defining what it should do, followed by a `:` and a `body` of data.

## Coordinate-based Actions

Assumed to work with relative offsets from each other. Coordinates are currently primarily specified in a dedicated file that specified what blocks need to be next to what other blocks, then evaluated by solving for positions that satisfy such requirements.

`$(dir:start,end)` or `$(dir:end)`

* Relative translation from start to end coordinates.
* If only one is provided, it is evaluated with a start of 0 0 0.

`$(rot:from,to)`

* Facing direction of from into to in terms of north/south/east/west/up/down.
* Only valid when the blocks are known to be next to each other through other means.

`$(set:name,x,y,z)`

* Inline assignment of a coordinate given to a name
* Does not return any text

`$(alias:first,second)`

* Assigns referencing second to evaluate to the same thing as first.
* Primarily useful when first is an iterating group and you want to reference its current value (at the point of assigning an alias) without having to care what number it results to.
* Does not return any text

### Name format

There are two kinds of block coordinates that follow a specific format: individual and groups. An individual block is left alone and handled as-is with a name as long as the name does not invoke group behavior. A group block abstracts away making use of an incredibly specific coordinate into an iteration-based structure. Groups eventually evaluate to and can be referenced to by their name followed by a number (starting at 1). Instead of using name1 to set a specific command and name2 to set a different command, both commands are used with name and evaluated at runtime to determine which belongs to name1 and name2. Formatting around the name dictates grouping behavior and grouping references as follows:

* Prepending a name with a + indicates you want it to behave as a group and to begins sequencing that name. Optionally a number can be placed immediately before the + to determine how much to increment it by.
* Appending a name with ±num evaluates to the group's block before or after that many times from the current id in iteration. Appending ± without a number afterwards is equivalent to ±1.
* If you do not prepend a name with a +, the result id is referenced from whatever the current iteration of the group is. When it is prepended with a +, the group index is iterated and then relative behavior is applied after the fact.

#### Example:

```
+name name name+1
+name name name-1
2+name name-2 name-1
+name-1 name name1
```

#### Will evaluate to:

```
name1 name1 name2
name2 name2 name1
name4 name2 name3
name4 name5 name1
```

> \* If the blocks are properly used in actions. This example just demonstrates how the order of the names and their relative contexts are applied.

#### Note:

```
$(name2-1) and $(+name2)
```

Are invalid and undefined uses, because you reference name2 explicitly and then attempt to apply behavior to it that assumes the context of a current iterating block in the group.

This formatting means that it is invalid and unreliable to begin a name with a +, end it with +- (optional numbers afterwards), or end it with numbers if you do not specifically intend to invoke group behavior with that particular name.

## Raw Data Insertion

`$(data:key)`

Inserts raw external data given by a key in a dictionary of provided values.

## Comments

`$(#comment text)`
Actions beginning with a # are comments and are evaluated to nothing.

`$(anything)`

Actions prepended with a backslash outside of the action are interpreted as literal text and no action behavior is applied.

### Non-action comments

* Single-line comments can be done in either python (#) or c (//) style
* Multi-line commenst can be done in either python (three " or ') or c (/* then */) style
* Both comments currenty only support commenting if the comment is at the start of a line.
