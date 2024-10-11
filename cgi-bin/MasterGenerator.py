#!/usr/bin/python3
import sys
import json
import cgi
import random

from GameObject import Terrain

from Terrain import Wall, Pit, Water, Fire, Spikes, EmptySpace  
from Decor import Stairs, Door
from Creatures import Goblin
from GameObject import Creature, CreatureSegment, Gold
from Items import IronDagger, WoodenClub

def generateMap(algorithm_index,uuid, depth):
    if algorithm_index != 2:
        if algorithm_index == 0:
            from GenerateMap import generateMap
        if algorithm_index == 1:
            from PathCarvedMap import generateMap
        saveMap(uuid, generateMap(10 + 2*depth,10 + 2*depth,depth,depth))
    else:
        from GenerateBoss import generateMap
        with open("../maps/"+uuid+".json", 'w') as file:
            json.dump(generateMap(depth), file)
        
        


def saveMap(uuid, final_grid):
    
    dictGrid = []
    
    for i in range(len(final_grid)):
        tempGrid = []
        for j in range(len(final_grid[0])):
            internalGrid = {gameObject.__class__.__base__.__name__.lower(): gameObject.__dict__ for gameObject in final_grid[i][j]}
            if (internalGrid.get('creature') is not None):
                internalGrid['creature']['equipment'] = ""
                internalGrid['creature']['drop_table'] = ""
            else:
                internalGrid["creature"] = {"textureIndex":8}
            tempGrid.append(internalGrid)
        dictGrid.append(tempGrid)
    
    json_grid = json.dumps(dictGrid)
    with open("../maps/"+uuid+".json", "w") as json_file:
        json_file.write(json_grid)
