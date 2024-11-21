#!/usr/bin/python3
import sys
import cgi
from GameObject import *
from SubSystem import *
import Level

class Wall(Terrain):
    def __init__(self, pos):
        super().__init__("Wall", "6", pos, 200, (0.7, 0.9, 1.0, 1.0, 0.7, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, False, "")

class Pit(Terrain):
    def __init__(self, pos):
        super().__init__("Pit", "18", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, False, "Are you sure you want to fall that far?")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        not_flying = True
        for status in creature.status_effects:
            if status.status_type == "Flight":
                not_flying = False
        if not_flying:
            creature.hp -= int((1.0-creature.damage_resistances[lookup_damage_type_id("BLT")]))
            #load new level
#cave, mine, corruptite mine, deep cavern: uncommonly
#cove, sewer: very commonly
class Water(Terrain):
    def __init__(self, pos):
        super().__init__("Shallow Water", "2", pos, 100, (1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, False, "")
    def on_step(self, grid, creature):
        for status in creature.status_effects:
            if status.status_type == "Flight":
                return
        creature.hp -= int(5*(1.0-creature.damage_resistances[lookup_damage_type_id("WTR")]))
        for status in creature.status_effects:
            if status.status_type == "Burning":
                creature.status_effects.remove(status)

#cave, cove: commonly
class LightBeam(LightTerrain):
    def __init__(self, pos):
        super().__init__("Light Beam", "23", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "", 8, True)
    def on_step(self, grid, creature):
        creature.hp -= int(50*(1.0-creature.damage_resistances[lookup_damage_type_id("LT")]))

#cove, sewer
class DeepWater(Terrain):
    def __init__(self, pos):
        super().__init__("Deep Water", "2", pos, 100, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, False, "Start swimming?")
    def on_step(self, grid, creature):
        for status in creature.status_effects:
            if status.status_type == "Flight":
                return
        creature.hp -= int(5*(1.0-creature.damage_resistances[lookup_damage_type_id("WTR")]))
        creature.gain_status_effect(grid,grid, lookup_status_resistance_id("Suffocation"), 5*(1-creature.damage_resistances[lookup_status_resistance_id("Suffocation")]), False)
        for status in creature.status_effects:
            if status.status_type == "Burning":
                creature.status_effects.remove(status)

#magma core, underworld: common
class Fire(LightTerrain):
    def __init__(self, pos):
        super().__init__("Fire", "51", pos, 10, (1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "Step into the flames?", 32, True)
    def on_step(self, grid, creature):
        for status in creature.status_effects:
            if status.status_type == "Flight":
                return
        creature.hp -= int(10*(1.0-creature.damage_resistances[lookup_damage_type_id("Fire")]))
        creature.gain_status_effect(grid, "Burning", 5*(1-creature.status_resistances[lookup_status_resistance_id("Burning")]), False, True, None)

    
#magma core, underworld: very common
class Lava(LightTerrain):
    def __init__(self, pos):
        super().__init__("Lava", "20", pos, 100, (1.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "Swim in the lava?", 32, True)
    def on_step(self, grid, creature):
        for status in creature.status_effects:
            if status.status_type == "Flight":
                return
        creature.hp -= int(100*(1.0-creature.damage_resistances[lookup_damage_type_id("Fire")]))
        creature.gain_status_effect(grid, "Burning", 50*(1-creature.status_resistances[lookup_status_resistance_id("Burning")]), False, True, None)

#temple of the old ones, uncommon
class Spikes(Terrain):
    def __init__(self, pos):
        super().__init__("Spikes", "21", pos, 20, (0.9, 0.2, 0.5, 1.0, 0.3, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, True, False, "Step onto the spikes?")
    def on_step(self, grid, creature):
        for status in creature.status_effects:
            if status.status_type == "Flight":
                return
        creature.hp -= int(20*(1.0-creature.damage_resistances[lookup_damage_type_id("Piercing")]))

#carrion: common
class Blood(Terrain):
    def __init__(self, pos):
        super().__init__("Blood", "2", pos, 100, (1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, False, "")
    def on_step(self, grid, creature):
        for status in creature.status_effects:
            if status.status_type == "Flight":
                return
        creature.hp -= int(5*(1.0-creature.damage_resistances[lookup_damage_type_id("WTR")]))

#worldeater's gut: common
class WorldeaterBile(Terrain):
    def __init__(self, pos):
        super().__init__("Bile", "2", pos, 100, (1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, False, "Swim in the acidic bile?")
    def on_step(self, grid, creature):
        for status in creature.status_effects:
            if status.status_type == "Flight":
                return
        creature.hp -= int(50*(1.0-creature.damage_resistances[lookup_damage_type_id("AD")]))
        acid_destroy(grid, creature, int(50*(1.0-creature.damage_resistances[lookup_damage_type_id("AD")])))

#main tile of ancient city
class MysticMist(LightTerrain):
    def __init__(self, pos):
        super().__init__("Mist", "20", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), False, False, "", 128, True)

#only tile of cosmic void, everything in cosmic void must have an AbsoluteNothingness Terrain
class AbsoluteNothingness(Terrain):
    def __init__(self, pos):
        super().__init__("Nothing", "20", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, False, "")
    def on_step(self, grid, creature):
        if creature.equipment[lookup_equipment_slot("Left Finger")] is not None and creature.equipment[lookup_equipment_slot("Left Finger")].name != "Voidwalker's Ring" and creature.equipment[lookup_equipment_slot("Right Finger")] is not None and creature.equipment[lookup_equipment_slot("Right Finger")].name != "Voidwalker's Ring":
            creature.gain_status_effect(grid, "Suffocation", 100, False, True, None)
            creature.gain_status_effect(grid, "Nonexistence", 100, False, True, None)
            pass
   
class EmptySpace(Terrain):
    def __init__(self, pos):
        super().__init__("EmptySpace", "1", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, True, False, "")
    def on_creation(self, grid):
        pass
    def on_step(self, grid, creature):
        pass

#spells only

class PoisonFog(Terrain):
    def __init__(self, pos):
        super().__init__("Poison Fog", "2", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, True, True, "Enter the Poison Fog?")
    def on_step(self, grid, creature):
        creature.gain_status_effect(grid, "Poison", 5, False, True, None)
