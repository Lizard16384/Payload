"""Giving information to the brute force position calculator

This is the layout and limitations of what is expected when brute force calculating
how certain blocks with requirements on what must be next to what in a region can fit.

The format with which this data is provided is not final and I do not like it, but this is
how it is right now. Below is an example of making use of all of its features.

Note that sample_positions.txt is the saved file of what the brute force calculator
generates so that it is not necessary to recalculate every single time
"""

# This file is not part of sample script, it is simply instructions on what the position calculator expects

def return_data():
    # Setup blocks to be used. Assumed layout is to have a sequence of blocks in a group
    # And then modify them to interact with each other as needed by adding or removing
    # connections and individual blocks
    data = {"groups":[
                {"name":"chain","amount":4,"start":[],"end":["chain1"]},
                {"name":"testA","amount":3,"start":[],"end":[],"intersect":0},
                {"name":"testB","amount":4,"start":["testA3"],"end":[],"intersect":[0]},
                {"name":"testC","amount":5,"start":["testB4"],"end":[]},
            ],
            "extra_connections":[
                ["testB1","testB4"],  # asssert that these must be next to each other
                ["impulse","chain1"]
            ],
            "disconnections":[
                ["testB1","testB2"]  # remove connections within groups
            ],
            "individual":[
                {"name":"impulse","start":[],"end":[]}  # no automatic group index behavior
            ]
            ,"offsets":[
                {"from":"impulse","to":"testA1","offset":[0,2,0]}  # relative locational requirements
            ]
            }

    # 
    conditionals = [["testC1","testC2","testC3"]]  # straight line enforcement to allow a line in any direction
        # - useful if testC2 needs to be conditional to what happens in testC1 and go to testC3

    # Define the area to work with
    size = {"x":3,"y":4,"z":3}

    fixed_positions = {"impulse":[1,0,1]}  # fixed positions for anything in the allowed region

    origin = [1,-1,1]  # final adjustment of positions before positions are used
        # shifts everything so that the origin is the new 0 0 0 before writing the resulting positions
        # does not matter for relative offsets from one thing to another, but sometimes nice to assume a default start location

    return data, fixed_positions, conditionals, size, origin  # inefficient way of getting the data to the necessary script
