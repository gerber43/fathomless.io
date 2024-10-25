#!/usr/bin/python3
import random
import sys
import cgi
import math
from abc import abstractmethod

damageTypes = ["Piercing","PRC","Slashing","SLH","Blunt","BLT","Fire","FR","Lightning","LTG","Water","WTR","Cold","CL","Acid","AD","Light","LT","Dark","DK","Necrotic","NCT","Arcane","AC","Existence","EXS"]
statusEffects = ["Bleed","Stun","Burning","Suffocation","Frozen","Blindness","Rot","Manaburn","Nonexistence","Poison","Fear","Confusion","Mindbreak","Midas Curse","Bloodsiphon","Manadrain","Death"]
critStatusEffects = ["Bleed","Bleed","Stun","Burning","Burning","Suffocation","Frozen","Blindness","Blindness","Rot","Manaburn","Nonexistence"]
skillIds = ["One-Handed Blades","One-Handed Blade","One-Handed Axes","One-Handed Axe","One-Handed Maces","One-Handed Mace","Two-Handed Blades","Two-Handed Blade","Two-Handed Axes","Two-Handed Axe","Two-Handed Maces","Two-Handed Mace","Polearms","Polearm","Slings","Sling","Bows","Bow","Elementalism","Elemental","Cursing","Curse","Enhancement","Enhancement","Transmutation","Transmute","Summoning","Summon","Dual-Wielding","Dual-Wielding","Memory","Memory","Search","Search","Hide","Hide","Lockpicking","Lockpick","Disarm Trap","Disarm"]
equipmentSlots = ["Right Hand","Left Hand","Head","Torso","Legs","Feet","Hands","Neck","Right Finger","Left Finger"]
#damage type and resistance subsystem, resistances are represented by a tuple of floats, use the following methods to figure out the indexes of specific  damage types and resistances
def lookup_damage_type_id(damage_type):
    if damage_type in damageTypes:
        return math.floor(damageTypes.index(damage_type) / 2)
    else:
        return -1
#Status effect subsystem
class StatusEffect:
    def __init__(self, status_type, stacks, infinite):
        self.status_type = status_type
        self.stacks = stacks
        self.infinite = infinite
    def on_apply(self, grid, creature):
        pass
    @abstractmethod
    def tick(self, grid, creature):
        if not self.infinite:
            self.stacks -= 1
        if self.stacks == 0:
            self.on_remove(grid, creature)
            creature.status_effects.remove(self)
    def on_remove(self, grid, creature):
        pass

def lookup_status_resistance_id(status_effect):
    if status_effect in statusEffects:
        return statusEffects.index(status_effect)
    else:
        return -1
        
def lookup_crit_status_effect(type_id):
    if type_id in critStatusEffects:
        return critStatusEffects.index(type_id)
    else:
        return -1

#skill subsystem, skills are represented by a tuple of integers, use the following methods to figure out the indexes of specific skills
def lookup_skill_id(skill):
    if skill in skillIds:
        return math.floor(skillIds.index(skill)/2)
    else:
        return -1

#equipment subsystem
def lookup_equipment_slot(slot):
    if slot in equipmentSlots:
        equipmentSlots.index(slot)
    else:
        return -1

#range-checking subsystem
def manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos1[1])

#active ability subsystem
class ActiveAbility:
    def __init__(self, name, textureIndex, level, cooldown, mp_cost, requirement):
        self.name = name
        self.textureIndex = textureIndex
        self.level = level
        self.cooldown = cooldown
        self.turns_left = 0
        self.mp_cost = mp_cost
        self.requirement = requirement
    #front-end should validate that turns_left = 0 and player.mp >= mp_cost before calling use
    @abstractmethod
    def use(self, grid, caster, target):
        self.turns_left = self.cooldown

class Prayer(ActiveAbility):
    def __init__(self, name, textureIndex, level, cooldown):
        super().__init__(name, textureIndex, level, cooldown, 0, None)
    @abstractmethod
    def use(self, grid, caster, target):
        super().use(grid, caster, target)

class Spell(ActiveAbility):
    def __init__(self, name, textureIndex, level, mp_cost, magic_school):
        super().__init__(name, textureIndex, level, 0, mp_cost, magic_school)
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
        if isinstance(caster.equipment[0], Weapon) and caster.equipment[0].type == self.requirement:
            super().use(grid, caster, target)
            if caster.basic_attack_hit_check(grid, caster.equipment[0], target):
                return 0
        if isinstance(caster.equipment[1], Weapon) and caster.equipment[1].type == self.requirement:
            super().use(grid, caster, target)
            if caster.basic_attack_hit_check(grid, caster.equipment[1], target):
                return 1
        return -1
