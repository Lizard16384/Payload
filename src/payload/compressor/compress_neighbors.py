def return_data():
    # Restrictions
    data = {"groups":[
                {"name":"minecart","amount":2,"start":[],"end":[],"intersect":1},
                {"name":"init","amount":1,"start":["setup2"],"end":[]}, # e
                {"name":"rule","amount":11,"start":["init1"],"end":["rule1"]}, # o e e o e o e o e o e
                {"name":"out","amount":3,"start":[],"end":[]}, # o e e
                {"name":"num","amount":10,"start":[],"end":[]}, # o e o e e o e o e o
                {"name":"ench","amount":4,"start":[],"end":[]}, # e o e o
                #{"name":"result","amount":3,"start":[],"end":[]}, # e o o e o e o
                {"name":"final","amount":7,"start":[],"end":["end"]}, # e
                {"name":"setup","amount":7,"start":[],"end":["setup2"],"intersect":[0,1]}
            ],
            "extra_connections":[
                ["rule2","num1"],["rule2","out1"],["rule5","rule1"],["rule9","num1"],
                ["num8","num4"],["num6","num9"],["num10","rule3"],["num10","out3"],
                ["ench4","num5"],["ench4","out2"]
            ],
            "disconnections":[
                {"rule2","rule3"},
                {"out2","out3"},
                {"num4","num5"},{"num8","num9"},
            ],
            "individual":[
                {"name":"aio","start":[],"end":[]},
                {"name":"ench_go_rule","start":["rule7"],"end":["ench1"]}, # e
                {"name":"ench_go_out","start":["out3"],"end":["ench1"]}, # o
                {"name":"num_go_out","start":["out2"],"end":["final1"]}, # o
                {"name":"ench_go_num","start":["num4"],"end":["ench1"]}, # o
                {"name":"end","start":[],"end":[]},

                {"name":"extra_to_rule8","start":["ench4"],"end":["rule8"]},
                {"name":"odd_to_num1","start":["num_go_out"],"end":["num1"]}, # e
                ]
            ,"offsets":[
                {"from":"aio","to":"minecart1","offset":[0,1,0]},
                {"from":"minecart1","to":"minecart2","offset":[0,1,0]}
            ]
            } # e

    # Assumed that these are already neighbors.
    conditionals = []

    # Define the area to work with
    size = {"x":4,"y":4,"z":4}

    fixed_positions = {"aio":[2,0,2]}

    origin = [2,2,2]

    return data, fixed_positions, conditionals, size, origin