#!/usr/bin/python3
import sys
import cgi
from LevelMapGenerator import generate_level

class Biome:
    def __init__(self, generation_algorithm, default_terrain, exit_decor, creature_spawn_table, other_spawn_table):
        self.generation_algorithm = generation_algorithm
        #will be wall in most cases
        self.default_terrain = default_terrain
        #will be stairs in most cases
        self.exit_decor = exit_decor
        #will be a list of tuples of the creature's name and their spawn weight
        self.creature_spawn_table = creature_spawn_table
        #will be a list of tuples of special terrain or decor name and their spawn weight
        self.other_spawn_table = other_spawn_table

class Level:
    def __init__(self, depth, biome):
        self.depth = depth
        self.biome = biome
        self.grid = generate_level(depth, biome)
