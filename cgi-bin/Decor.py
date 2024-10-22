#!/usr/bin/python3
import sys
import cgi
from GameObject import Decor, LightDecor, spread_light
from Level import Level, Biome
from Biomes import TempBiome
from Items import Pebble, Ore, Corruptite
from Creatures import Ghost

class Corpse(Decor):
    def __init__(self, pos, hp, resistances):
        super().__init__("Corpse", "70", pos, hp, resistances, True, False, "NO", "")


class Stairs(Decor):
    def __init__(self, pos):
        super().__init__("Stairs", "23", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "Yes", "Go Down?")
    def on_interact(self, current_level, creature):
        if current_level.depth < 22:
            new_level = Level(current_level.depth+1, TempBiome())
            current_level.grid = new_level.grid
            current_level.depth = new_level.depth

#mine, corruptite mine, shantytown, undercity
class Door(Decor):
    def __init__(self, pos):
        super().__init__("Wooden Door", '24', pos, 40, (0.7, 0.7, 0.3, -1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_interact(self, grid, creature):
        if not self.passable:
            self.passable = True
            self.block_sight = False
        else:
            self.passable = False
            self.block_sight = True

#ziggurat, columbarium, catacomb, necropolis, temple of the old ones
class StoneDoor(Decor):
    def __init__(self, pos):
        super().__init__("Stone Door", "24", pos, 70, (0.7, 0.9, 1.0, 1.0, 0.7, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_interact(self, grid, creature):
        if not self.passable:
            self.passable = True
            self.block_sight = False
        else:
            self.passable = False
            self.block_sight = True

#cave, mines, cove corruptite mines, deep cavern: common
class Rock(Decor):
    def __init__(self, pos):
        super().__init__("Rock", "24", pos, 70, (0.7, 0.9, 1.0, 1.0, 0.7, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_destroy(self, grid):
        grid[self.pos[0]][self.pos[1]].append(Pebble(self.pos, 10))
        super().on_destroy(grid)

#cove: uncommon
class Coral(Decor):
    def __init__(self, pos):
        super().__init__("Coral", "24", pos, 40, (0.7, 0.9, 0.2, 1.0, 1.0, 1.0, 1.0, 0.1, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")

# mines, corruptite mines: uncommon
class Deposit(Decor):
    def __init__(self, pos):
        super().__init__("Mineral Deposit", "24", pos, 70, (0.7, 0.9, 1.0, 1.0, 0.7, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_destroy(self, grid):
        grid[self.pos[0]][self.pos[1]].append(Ore(self.pos, 5))
        super().on_destroy(grid)

#corruptite mines: rare
class CorruptiteCluster(Decor):
    def __init__(self, pos):
        super().__init__("Corruptite Cluster", "24", pos, 40, (0.7, 0.9, 0.2, 1.0, 1.0, 1.0, 1.0, 0.1, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_destroy(self, grid):
        grid[self.pos[0]][self.pos[1]].append(Corruptite(self.pos, 3))
        super().on_destroy(grid)

#columbarium: common
#catacombs: uncommon
class Urn(Decor):
    def __init__(self, pos):
        super().__init__("Burial Urn", "24", pos, 10, (0.0, 0.5, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_destroy(self, grid):
        grid[self.pos[0]][self.pos[1]].append(Ghost(self.pos))
        super().on_destroy(grid)

#mine, corruptite mine, sewer, shantytown, ziggurat: common
class StandingTorch(LightDecor):
    def __init__(self, grid, pos):
        super().__init__(grid, "Torch", "24", pos, 5, (0.7, 0.7, 0.3, -1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, "NO", "", 32, True)

#embers: common
class Ember(LightDecor):
    def __init__(self, grid, pos):
        super().__init__(grid, "Ember", "24", pos, 5, (0.7, 0.9, 1.0, 1.0, 0.7, 0.0, -1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, "NO", "", 16, True)

#carrion, worldeater's gut: common
class LightGrowth(LightDecor):
    def __init__(self, grid, pos):
        super().__init__(grid, "Growth", "24", pos, 60, (0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0), False, "NO", "", 32, True)


#columbarium, catacombs, necropolis: common
class SpiritLight(LightDecor):
    def __init__(self, grid, pos):
        super().__init__(grid, "Spirit Light", "24", pos, 5, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0), True, "NO", "", 16, True)

#cosmic void: common
class Energy(LightDecor):
    def __init__(self, grid, pos):
        super().__init__(grid, "Energy", "24", pos, 200, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0), True, "NO", "", 128, True)
