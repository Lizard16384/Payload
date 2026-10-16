def return_data():
    # Restrictions
    data = {"groups":[
                {"name":"minecart","amount":2,"start":[],"end":[],"intersect":1},
                {"name":"init","amount":6,"start":["setup2"],"end":["init1"]}, # o e o e o e
                {"name":"rule","amount":11,"start":["init6"],"end":["rule1"]}, # o e e o e o e o e o e
                {"name":"out","amount":3,"start":[],"end":[]}, # o e e
                {"name":"num","amount":6,"start":[],"end":[]}, # o e o e e o
                {"name":"ench","amount":6,"start":[],"end":[]}, # e o e o
                {"name":"final","amount":4,"start":[],"end":["destroy1"]}, # e o e o
                {"name":"destroy","amount":8,"start":[],"end":["end"]}, # e o e o e o e o
                {"name":"setup","amount":7,"start":[],"end":["setup2"],"intersect":[0,1]} # o e o e o e o
            ],
            "extra_connections":[
                ["rule2","num1"],["rule2","out1"],["rule5","rule1"],["rule9","num1"],
                ["num6","rule3"],["num6","out3"],
                ["ench6","num5"],["ench6","out2"],["ench1","init3"],["ench6","init4"],
                ["gamerule","setup1"]
            ],
            "disconnections":[
                {"rule2","rule3"},{"rule7","rule8"},
                {"out2","out3"},
                {"num4","num5"},
            ],
            "individual":[
                {"name":"gamerule","start":["setup1"],"end":[]}, # e
                {"name":"aio","start":[],"end":[]},
                {"name":"ench_go_rule","start":["rule7"],"end":["ench1"]}, # o
                {"name":"ench_go_out","start":["out3"],"end":["ench1"]}, # o
                {"name":"num_go_out","start":["out2"],"end":["final1"]}, # o
                {"name":"ench_go_num","start":["num4"],"end":["ench1"]}, # o
                {"name":"end","start":[],"end":[]},

                {"name":"extra_to_rule8","start":["ench6"],"end":["rule8"]}, # e
                {"name":"odd_to_num1","start":["num_go_out"],"end":["num1"]}, # e

                {"name":"destroy_backup","start":["setup1"],"end":[]},
                {"name":"destroy_backup_chain","start":["destroy_backup"],"end":["destroy1"]}
                ]
            ,"offsets":[
                {"from":"aio","to":"minecart1","offset":[0,1,0]},
                {"from":"minecart1","to":"minecart2","offset":[0,1,0]}
            ]
            } # e

    # Assumed that these are already neighbors.
    conditionals = [["gamerule","setup1","destroy_backup"]]

    # Define the area to work with
    size = {"x":5,"y":5,"z":5}

    fixed_positions = {"aio":[2,0,2]}

    origin = [2,2,2]

    return data, fixed_positions, conditionals, size, origin