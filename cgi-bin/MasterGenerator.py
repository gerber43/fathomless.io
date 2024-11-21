def generateMap(algorithm_index,depth,player):
    depths = depth.split(",")
    depths[0] = int(depths[0])
    multipier = 1
    if (depths[1] == "medium"):
        multipier = 2
    if (depths[1] == "hard"):
        multipier = 3
    if depths[0] == 0:
        algorithm_index = 2
    if algorithm_index == 0:
        from GenerateMap import generateMap
    if algorithm_index == 1:
        from PathCarvedMap import generateMap
    if algorithm_index == 2:
        from GenerateLevelZero import generateMap
    dimension = 10 + 2*int(depths[0]) if (depths[1] != "Test" and depths[0] != 22) else 20
    final_grid = generateMap(dimension, dimension ,depth, multipier*(depths[0] + 1),player,depths[0]//multipier)
    return final_grid
