#!/usr/bin/python3
import sys
import json
import cgi
import random
import pickle
from GameObject import Terrain

from Terrain import Wall, Pit, Water, Fire, Spikes, EmptySpace  
from Decor import Stairs, Door
from Creatures import Goblin
from GameObject import Creature, CreatureSegment, Gold
from Items import IronDagger, WoodenClub

def save_pickle(map_file_path, map_data):
    with open(map_file_path, 'wb') as pickle_file:
        pickle.dump(map_data, pickle_file)
    
        
def load_pickle(map_file_path):
    with open(map_file_path, 'rb') as pickle_file:
        return pickle.load(pickle_file)


def generateMap(algorithm_index,uuid,depth):
    depths = depth.split(",")
    multipier = 1
    if (depths[1] == "medium"):
        multipier = 2
    if (depths[1] == "hard"):
        multipier = 3

    if algorithm_index != 2:
        if algorithm_index == 0:
            from GenerateMap import generateMap
        if algorithm_index == 1:
            from PathCarvedMap import generateMap
        final_grid = generateMap(10 + 2*int(depths[0]), 10 + 2*int(depths[0]) ,depth, multipier*int(depths[0]))
        saveMap(uuid, final_grid)
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
    save_pickle("../maps/"+uuid+".pkl",final_grid)
