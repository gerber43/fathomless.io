#!/usr/bin/python3
import sys
import json
import cgi
import random

HTTP_FIELDS = cgi.FieldStorage()

from GameObject import Terrain

from Terrain import Wall, Pit, Water, Fire, Spikes, EmptySpace  

def generateMap(algorithm_index,uuid):
    if algorithm_index == 0:
        from GenerateMap import generateMap
    if algorithm_index == 1:
        from PathCarvedMap import generateMap
    saveMap(uuid, generateMap())


def saveMap(uuid, final_grid):
    dictGrid = []
    for i in range(len(final_grid)):
        tempGrid = []
        for j in range(len(final_grid[0])):
            if (final_grid[i][j]):
                tempGrid.append({"terrain": final_grid[i][j].__dict__,"entity": {"textureIndex":8}})
            else: 
                tempGrid.append({"terrain": EmptySpace((i, j)).__dict__,"entity": {"textureIndex":8}})
        dictGrid.append(tempGrid)
    dictGrid[0][0]['entity'] = {"textureIndex":0}
    json_grid = json.dumps(dictGrid)
    with open("../maps/"+uuid+".json", "w") as json_file:
        json_file.write(json_grid)
