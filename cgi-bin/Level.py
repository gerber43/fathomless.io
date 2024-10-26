#!/usr/bin/python3
import random
import sys
import cgi
from LevelMapGenerator import generate_level

class Biome:
    def __init__(self, generation_algorithm, default_terrain, exit_decor, creature_spawn_table, other_spawn_table, boss, boss_depth):
        self.generation_algorithm = generation_algorithm
        #will be wall in most cases
        self.default_terrain = default_terrain
        #will be stairs in most cases
        self.exit_decor = exit_decor
        #will be a list of tuples of the creature's name and their spawn weight
        self.creature_spawn_table = creature_spawn_table
        #will be a list of special terrain or decor name, no weight since spawn conditions are environmental
        self.other_spawn_table = other_spawn_table
        #pointer to the boss, biomes without a boss have None
        self.boss = boss
        #the depth at which the boss spawns at, biomes without a boss have -1
        self.boss_depth = boss_depth
    def random_creature(self):
        num_creatures = len(self.creature_spawn_table)
        index = random.randint(0, num_creatures - 1)
        min_weight = random.random()
        while self.creature_spawn_table[index][1] < min_weight:
            index = random.randint(0, num_creatures - 1)
            min_weight = random.random()
        return self.creature_spawn_table[index][0]

class Level:
    def __init__(self, depth, biome):
        self.depth = depth
        self.biome = biome
        self.grid = generate_level(depth, biome)
