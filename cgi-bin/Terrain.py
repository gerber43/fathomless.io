#!/usr/bin/python3
import sys
import cgi
from GameObject import Terrain
from SubSystem import lookup_status_effect_id
import Level

class Wall(Terrain):
    def __init__(self, pos):
        super().__init__("Wall", "#", pos, 200, (0.7, 0.9, 1.0, 1.0, 0.7, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        pass

class Pit(Terrain):
    def __init__(self, pos):
        super().__init__("Pit", "", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "WALK", "Are you sure you want to fall that far?")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        flight_id = lookup_status_effect_id("Flight")
        not_flying = True
        for status in creature.status_effects:
            if status.type_id == flight_id:
                not_flying = False
        if not_flying:
            creature.hp -= 200*(1-creature.resistances.getResistance("BLT"))
            #load new level
class Water(Terrain):
    def __init__(self, pos):
        super().__init__("Wall", "#", pos, 200, (0.7, 0.9, 1.0, 1.0, 0.7, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        pass
class Fire(Terrain):
    def __init__(self, pos):
        super().__init__("Wall", "#", pos, 200, (0.7, 0.9, 1.0, 1.0, 0.7, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        creature.lose_health(10)
        pass
class Spikes(Terrain):
    def __init__(self, pos):
        super().__init__("Wall", "#", pos, 200, (0.7, 0.9, 1.0, 1.0, 0.7, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        creature.lose_health(10)
       pass
class EmptySpace(Terrain):
    def __init__(self, pos):
        super().__init__("Wall", "#", pos, 200, (0.7, 0.9, 1.0, 1.0, 0.7, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        pass
