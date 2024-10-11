#!/usr/bin/python3
import sys
import json
import cgi
import random

HTTP_FIELDS = cgi.FieldStorage()

from GameObject import Terrain, Decor, Creature
from Terrain import Wall, Pit, Water, Fire, Spikes, EmptySpace  
from Decor import Stairs, Door
from Creatures import Goblin, Player, Boss


def load_map(map_file_path):
    with open(map_file_path, 'r') as file:
        return json.load(file)

#Funciton to save the updated map
def save_map(map_file_path, map_data):
    with open(map_file_path, 'w') as file:
        json.dump(map_data, file)
        
def generateMap(depth):
    randomInt = random.randint(0, 1)
    bossMap = load_map("../json/boss_map.json" if (randomInt == 0) else "../json/boss_map2.json")
    for i in range(len(bossMap)):
        for j in range(len(bossMap[0])):
            bossMap[i][j]['creature'] = {"textureIndex": 8}
    if (randomInt == 0):
        
        bossMap[0][0]['creature'] = Player((0, 0))
        bossMap[6][6]['creature'] = Boss((6,6))
        bossMap[0][0]['creature'].equipment = ""
        bossMap[0][0]['creature'].drop_table = ""
        bossMap[6][6]['creature'].equipment = ""
        bossMap[6][6]['creature'].drop_table = ""
        bossMap[0][0]['creature'] = bossMap[0][0]['creature'].__dict__
        bossMap[6][6]['creature'] = bossMap[6][6]['creature'].__dict__
        stair = Stairs((9, 9))
        stair.hp = depth
        bossMap[9][9]['decor'] = stair.__dict__
        
    else:
        bossMap[12][3]['creature'] = Player((0, 0))
        bossMap[6][6]['creature'] = Boss((6,6))
        bossMap[12][3]['creature'].equipment = ""
        bossMap[12][3]['creature'].drop_table = ""
        bossMap[6][6]['creature'].equipment = ""
        bossMap[6][6]['creature'].drop_table = ""
        bossMap[12][3]['creature'] = bossMap[12][3]['creature'].__dict__
        bossMap[6][6]['creature'] = bossMap[6][6]['creature'].__dict__
        stair = Stairs((9, 9))
        stair.hp = depth
        bossMap[9][9]['decor'] = stair.__dict__
    return(bossMap)

