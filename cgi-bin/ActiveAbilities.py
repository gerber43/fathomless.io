#!/usr/bin/python3
import sys
import cgi
import math
import random
from abc import abstractmethod
from GameObject import Weapon
from SubSystem import lookup_damage_type_id
from Terrain import DeepWater

#Active ability base classes
class ActiveAbility:
    def __init__(self, name, textureIndex, level, cooldown, mp_cost, range, requirement):
        self.name = name
        self.textureIndex = textureIndex
        self.level = level
        self.cooldown = cooldown
        self.turns_left = 0
        self.mp_cost = mp_cost
        self.range = range
        self.requirement = requirement
    #front-end should validate that turns_left = 0 and player.mp >= mp_cost before calling use
    @abstractmethod
    def use(self, grid, caster, target):
        self.turns_left = self.cooldown

class Prayer(ActiveAbility):
    def __init__(self, name, textureIndex, level, cooldown, range):
        super().__init__(name, textureIndex, level, cooldown, range, 0, None)
    @abstractmethod
    def use(self, grid, caster, target):
        super().use(grid, caster, target)

class Spell(ActiveAbility):
    def __init__(self, name, textureIndex, level, mp_cost, range, magic_school):
        super().__init__(name, textureIndex, level, 0, mp_cost, range, magic_school)
    @abstractmethod
    def use(self, grid, caster, target):
        caster.mp -= self.mp_cost
        equip_weight = 0
        for item in caster.equipment:
            if item is not None:
                equip_weight += item.weight
        success_chance = (0.75*math.log10(float(self.requirement)))-(0.005*equip_weight)
        failure_roll = random.random
        if failure_roll > success_chance:
            return False
        return True

class Technique(ActiveAbility):
    def __init__(self, name, textureIndex, level, cooldown, weapon_type):
        super().__init__(name, textureIndex, level, cooldown, 0, weapon_type)
    @abstractmethod
    def use(self, grid, caster, target):
        num_hits = 0
        if isinstance(caster.equipment[0], Weapon) and caster.equipment[0].type == self.requirement:
            super().use(grid, caster, target)
            if caster.basic_attack_hit_check(grid, caster.equipment[0], isinstance(caster.equipment[1], Weapon), target):
                num_hits = num_hits + 1
        if isinstance(caster.equipment[1], Weapon) and caster.equipment[1].type == self.requirement:
            super().use(grid, caster, target)
            if caster.basic_attack_hit_check(grid, caster.equipment[1], isinstance(caster.equipment[0], Weapon), target):
                num_hits = num_hits + 1
        return num_hits

#player racial active abilities

class Blink(ActiveAbility):
    def __init__(self):
        super().__init__("Blink", "1", 0, 20, 0, 3, "")
    #target in this case is a grid location
    def use(self, grid, caster, target):
        grid[target[0]][target[1]].append(caster)
        grid[caster.pos[0]][caster.pos[1]].remove(caster)
        caster.pos = target
        super().use(self, grid, caster, target)

class Berserking(ActiveAbility):
    def __init__(self):
        super().__init__("Berserking", "1", 0, 50, 0, 0, "")
    #target in this case is a grid location
    def use(self, grid, caster, target):
        caster.gain_status_effect(grid, "Berserk", 20, False, False, None)
        super().use(self, grid, caster, target)

class Torture(ActiveAbility):
    def __init__(self):
        super().__init__("Torture", "1", 0, 30, 0, 3, "")
    #target in this case is a grid location
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "Bleed", 3, False, True, None)
        super().use(self, grid, caster, target)


#player-available spells

class IceBolt(Spell):
    def __init__(self):
        super().__init__("Healing Touch", "45", 2, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target.hp -= 5*target.resistances(lookup_damage_type_id("Cold"))
        super().use(grid, caster, target)

class HealingTouch(Spell):
    def __init__(self):
        super().__init__("Healing Touch", "45", 3, 20, 1, "Enhancement")
    def use(self, grid, caster, target):
        target.hp = target.max_hp
        super().use(grid, caster, target)

#player-available techniques

#prayers

#enemy-only active abilities

#enemy-only spells

class ChokingDeep(Spell):
    def __init__(self):
        super().__init__("Choking Deep", "45", 4, 5, 7, "Cursing")
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "Suffocation", 10, False, True, None)
        super().use(grid, caster, target)

class TidalWave(Spell):
    def __init__(self):
        super().__init__("Tidal Wave", "45", 8, 20, 5, "Elementalism")
    def use(self, grid, caster, target):
        for i in range(1):
            for j in range(1):
                grid[target.pos[0] + i][target.pos[0] + j].append(DeepWater([target.pos[0] + i, target.pos[0] + j]))
                grid[target.pos[0] - i][target.pos[0] + j].append(DeepWater([target.pos[0] - i, target.pos[0] + j]))
                grid[target.pos[0] + i][target.pos[0] - j].append(DeepWater([target.pos[0] + i, target.pos[0] - j]))
                grid[target.pos[0] - i][target.pos[0] - j].append(DeepWater([target.pos[0] - i, target.pos[0] - j]))

#enemy-only techniques
