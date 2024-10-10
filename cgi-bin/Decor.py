#!/usr/bin/python3
import sys
import cgi
from GameObject import Decor
from Level import Level, Biome
from Biomes import TempBiome

class Door(Decor):
    def __init__(self, pos):
        super().__init__("Door", 'D', pos, 40, (0.7, 0.7, 0.3, -1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_interact(self, grid, creature):
        if not self.passable:
            self.passable = True
            self.block_sight = False
        else:
            self.passable = False
            self.block_sight = True
    def passive_behavior(self, grid):
        pass

class Stairs(Decor):
    def __init__(self, pos):
        super().__init__("Stairs", "=", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "Yes", "Go Down?")
    def on_interact(self, current_level, creature):
        #TODO: load new level and change to the new level
        if current_level.depth < 22:
            new_level = Level(current_level.depth+1, TempBiome())
            current_level.grid = new_level.grid
            current_level.depth = new_level.depth
        pass
    def passive_behavior(self, grid):
        pass
