#!/usr/bin/python3
import sys
import cgi
from LevelMapGenerator import generate_level

class Level:
    def __init__(self, width, height, depth, biome):
        self.width = width
        self.height = height
        self.depth = depth
        self.biome = biome
        self.grid = generate_level(width, height, depth, biome)
