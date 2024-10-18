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

def generateMap(algorithm_index,depth):
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
    final_grid = generateMap(10 + 2*int(depths[0]), 10 + 2*int(depths[0]) ,depth, multipier*int(depths[0]))
    return final_grid
