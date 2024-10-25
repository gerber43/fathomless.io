#!/usr/bin/python3
import sys
import cgi
from GameObject import *
from SubSystem import *
import Level

class Wall(Terrain):
    def __init__(self, pos):
        super().__init__("Wall", "6", pos, 200, (0.7, 0.9, 1.0, 1.0, 0.7, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")

class Pit(Terrain):
    def __init__(self, pos):
        super().__init__("Pit", "18", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "WALK", "Are you sure you want to fall that far?")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        not_flying = True
        for status in creature.status_effects:
            if status.status_type == "Flight":
                not_flying = False
        if not_flying:
            creature.hp -= 200*(1.0-creature.damage_resistances[lookup_damage_type_id("BLT")])
            #load new level
#cave, mine, corruptite mine, deep cavern: uncommonly
#cove, sewer: very commonly
class Water(Terrain):
    def __init__(self, pos):
        super().__init__("Shallow Water", "2", pos, 100, (1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "NO", "")
    def on_step(self, grid, creature):
        creature.hp -= 5*(1.0-creature.damage_resistances[lookup_damage_type_id("WTR")])

#cave, cove: commonly
class LightBeam(LightTerrain):
    def __init__(self, grid, pos):
        super().__init__(grid, "Light Beam", "23", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, "NO", "", 8, True)
    def on_step(self, grid, creature):
        creature.hp -= 50*(1.0-creature.damage_resistances[lookup_damage_type_id("LT")])

#cove, sewer
class DeepWater(Terrain):
    def __init__(self, pos):
        super().__init__("Deep Water", "2", pos, 100, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "NO", "")
    def on_step(self, grid, creature):
        creature.hp -= 5*(1.0-creature.damage_resistances[lookup_damage_type_id("WTR")])
        creature.gain_status_effect(grid,grid, lookup_status_resistance_id("Suffocation"), 5*(1-creature.damage_resistances[lookup_status_resistance_id("Suffocation")]), False)
#magma core, underworld: common


class Fire(Terrain):
    def __init__(self, pos):
        super().__init__("Fire", "20", pos, 10, (1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, True, "NO", "")
    def on_step(self, grid, creature):
        creature.hp -= 10*(1.0-creature.damage_resistances[lookup_damage_type_id("Fire")])
        creature.gain_status_effect(grid,"Burning", 5*(1-creature.status_resistances[lookup_status_resistance_id("Burning")]))

    
#magma core, underworld: very common
class Lava(LightTerrain):
    def __init__(self, grid, pos):
        super().__init__(grid, "Lava", "20", pos, 100, (1.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, "NO", "", 32, True)
    def on_step(self, grid, creature):
        creature.hp -= 100*(1.0-creature.damage_resistances[lookup_damage_type_id("Fire")])
        creature.gain_status_effect(grid,lookup_status_resistance_id("Burning"), 50*(1-creature.status_resistances[lookup_status_resistance_id("Burning")]))


class Spikes(Terrain):
    def __init__(self, pos):
        super().__init__("Spikes", "21", pos, 20, (0.9, 0.2, 0.5, 1.0, 0.3, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, True, "NO", "")
    def on_step(self, grid, creature):
       creature.hp -= 20*(1.0-creature.damage_resistances[lookup_damage_type_id("Piercing")])

#carrion: common
class Blood(Terrain):
    def __init__(self, pos):
        super().__init__("Blood", "2", pos, 100, (1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "NO", "")
    def on_step(self, grid, creature):
        creature.hp -= 5*(1.0-creature.damage_resistances[lookup_damage_type_id("WTR")])

#worldeater's gut: common
class WorldeaterBile(Terrain):
    def __init__(self, pos):
        super().__init__("Bile", "2", pos, 100, (1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "NO", "")
    def on_step(self, grid, creature):
        creature.hp -= 100*(1.0-creature.damage_resistances[lookup_damage_type_id("AD")])

#main tile of ancient city
class MysticMist(LightTerrain):
    def __init__(self, grid, pos):
        super().__init__(grid, "Mist", "20", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), False, "NO", "", 128, True)

#only tile of cosmic void
class AbsoluteNothingness(Terrain):
    def __init__(self, pos):
        super().__init__("Nothing", "20", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, "NO", "No", "")
    def on_step(self, grid, creature):
        if creature.equipment[lookup_equipment_slot("Left Finger")] is not None and creature.equipment[lookup_equipment_slot("Left Finger")].name != "Voidwalker's Ring" and creature.equipment[lookup_equipment_slot("Right Finger")] is not None and creature.equipment[lookup_equipment_slot("Right Finger")].name != "Voidwalker's Ring":
            creature.gain_status_effect(grid,lookup_status_resistance_id("Suffocation"), 100, False)
            creature.gain_status_effect(grid,lookup_status_resistance_id("Nonexistence"), 100, False)
            pass
   
class EmptySpace(Terrain):
    def __init__(self, pos):
        super().__init__("EmptySpace", "1", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, True, "NO", "")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        pass
