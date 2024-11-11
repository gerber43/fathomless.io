def generateMap(algorithm_index,depth,player):
    depths = depth.split(",")
    multipier = 1
    if (depths[1] == "medium"):
        multipier = 2
    if (depths[1] == "hard"):
        multipier = 3

    if algorithm_index == 0:
        from GenerateMap import generateMap
    if algorithm_index == 1:
        from PathCarvedMap import generateMap
    dimension = 10 + 2*int(depths[0]) if (depths[1] != "Test" and int(depths[0]) != 22) else 20
    final_grid = generateMap(dimension, dimension ,depth, multipier*int(depths[0]),player,int(depths[0])//multipier)
    return final_grid
