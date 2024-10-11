#!/usr/bin/python3
import sys
import cgi
from GameObject import Terrain
from SubSystem import lookup_status_effect_id, lookup_damage_type_id
import Level

class Wall(Terrain):
    def __init__(self, pos):
        super().__init__("Wall", "6", pos, 200, (0.7, 0.9, 1.0, 1.0, 0.7, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        pass

class Pit(Terrain):
    def __init__(self, pos):
        super().__init__("Pit", "18", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "WALK", "Are you sure you want to fall that far?")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        flight_id = lookup_status_effect_id("Flight")
        not_flying = True
        for status in creature.status_effects:
            if status.type_id == flight_id:
                not_flying = False
        if not_flying:
            creature.hp -= 200*(1.0-creature.resistances[lookup_damage_type_id("BLT")])
            #load new level
class Water(Terrain):
    def __init__(self, pos):
        super().__init__("Shallow Water", "2", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "NO", "")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        creature.hp -= 5*(1.0-creature.resistances[lookup_damage_type_id("WTR")])
class Fire(Terrain):
    def __init__(self, pos):
        super().__init__("Fire", "20", pos, 10, (1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, True, "NO", "")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        creature.hp -= 5*(1.0-creature.resistances[lookup_damage_type_id("Fire")])
        pass
class Spikes(Terrain):
    def __init__(self, pos):
        super().__init__("Spikes", "21", pos, 20, (0.9, 0.2, 0.5, 1.0, 0.3, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
       creature.hp -= 20*(1.0-creature.resistances[lookup_damage_type_id("Piercing")])
       pass
class EmptySpace(Terrain):
    def __init__(self, pos):
        super().__init__("EmptySpace", "1", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, True, "NO", "")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        pass
