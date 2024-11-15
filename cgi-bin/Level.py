#!/usr/bin/python3
import random
import sys
import cgi

class Biome:
    def __init__(self, generation_algorithm, default_terrain, exit_decor, creature_spawns, creature_weights, other_spawns, other_weights, num_levels, biome_connections, boss, boss_level):
        self.generation_algorithm = generation_algorithm
        #will be wall in most cases
        self.default_terrain = default_terrain
        #will be stairs in most cases
        self.exit_decor = exit_decor
        #will be a list of the creatures' names
        self.creature_spawns = creature_spawns
        #will be a list of the creatures' spawn weights
        self.creature_weights = creature_weights
        #will be a list of special terrain or decor name, no weight since spawn conditions are environmental
        self.other_spawns = other_spawns
        # will be a list of special terrain or decor name, no weight since spawn conditions are environmental
        self.other_weights = other_weights
        #the number of levels in the biome
        self.num_levels = num_levels
        #a list of other biomes the biome connects to, represented by an array of tuples,
        #the first field of the tuple is the level of the current biome with the connection,
        #the second field is the biome it conneccts to,
        #and the third field is the level in the other biome that the connection leads to
        self.biome_connections = biome_connections
        #pointer to the boss, biomes without a boss have None
        self.boss = boss
        #on which of the biome's levels the boss spawns at, biomes without a boss have -1
        self.boss_level = boss_level
    def random_creature(self, pos):
        creature_name = random.choices(self.creature_spawns, self.creature_weights)
        return eval(creature_name)(pos)
    def random_other(self, pos):
        creature_name = random.choices(self.creature_spawns, self.creature_weights)
        return eval(creature_name)(pos)

class Level:
    def __init__(self, depth, biome):
        self.depth = depth
        self.biome = biome
        self.grid = generate_level(depth, biome)