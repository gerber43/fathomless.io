#!/usr/bin/python3
import sys
import cgi
from abc import abstractmethod
import random
from operator import truediv
from Subsystem import StatusEffect, lookup_crit_status_effect, lookup_skill_id


class GameObject:
    def __init__(self, name, symbol, pos):
        self.name = name
        self.symbol = symbol
        self.pos = pos

class Item(GameObject):
    def __init__(self, name, symbol, pos, level, price):
        super().__init__(name, symbol, pos)
        #The item's level is a general guide for how powerful it should be
        self.level = level
        #Price the item will be sold for in shops
        self.price = price

class Creature(GameObject):
    def __init__(self, name, symbol, pos, segments, hp, mp, speed, status_effects, fitness, cunning, magic, dodge, critChance, equipment, skills, abilities, damage_resistances, status_resistances, dropTable):
        super().__init__(name, symbol, pos)
        #list of creature segments, should be empty for single-tile creatures
        self.segments = segments
        self.hp = hp
        self.mp = mp
        self.speed = speed
        self.status_effects = status_effects
        self.fitness = fitness
        self.cunning = cunning
        self.magic = magic
        self.dodge = dodge
        self.critChance = critChance
        self.equipment = equipment
        self.skills = skills
        self.abilities = abilities
        self.damage_resistances = damage_resistances
        self.status_resistances = status_resistances
        self.dropTable = dropTable

    def gainStatusEffect(self, type_id, stacks, infinite):
        if stacks == 0:
            return
        for status in self.status_effects:
            if type_id == status.type_id:
                if status.infinite:
                    return
                if infinite:
                    status.infinite = True
                    status.stacks = stacks
                    return
                status.stacks += stacks
                return
        self.status_effects.append(type_id, stacks, infinite)

    def basic_attack_hit_check(self, weapon, target):
        #TODO: Implement ammo checking and ammo decrement
        if isinstance(target, CreatureSegment):
            target = target.creature
        hitChance = self.skills[lookup_skill_id(weapon.type)] - target.dodge
        hitRoll = random.random
        if hitRoll > hitChance:
            return False
        else:
            return True

    def crit_check(self):
        critRoll = random.random
        if critRoll < self.critChance:
            return False
        else:
            return True

    def basic_attack_damage(self, weapon, target, crit):
        for damage in weapon.damages:
            total = damage.base
            if crit:
                total = total*weapon.critMult
            else:
                total = total + random.randint(-damage.var, damage.var)
            if (damage.dmgtype == 0) or (damage.dmgtype == 1) or (damage.dmgtype == 2):
                total = total + self.fitness
            total = int(total * (1.0-target.damage_resistances[damage.dmgtype]))
            target.hp -= total
            if crit:
                target.gainStatusEffect(lookup_crit_status_effect(damage.dmgtype), total/10, False)
        for status in weapon.statuses:
            target.gainStatusEffect(status.type_id, status.stacks, status.infinite)

    def basic_attack(self, target):
        #TODO: apply dual wielding penalty if dual wielding
        if isinstance(self.equipment.right_hand, Weapon):
            if not self.basic_attack_hit_check(self.equipment.right_hand, target):
                return
            self.basic_attack_damage(self.equipment.right_hand, target, self.crit_check())
        if isinstance(self.equipment.left_hand, Weapon):
            if not self.basic_attack_hit_check(self.equipment.left_hand, target):
                return
            self.basic_attack_damage(self.equipment.left_hand, target, self.crit_check())

    #will be overloaded in player class to accept input from frontend
    #will be overloaded in all NPC classes with their AI
    @abstractmethod
    def next_action(self):
        pass

#support multi-tile creatures
class CreatureSegment(GameObject):
    def __init__(self, creature, symbol, pos):
        super().__init__(creature.name, symbol, pos)
        self.creature = creature

class Consumable(Item):
    def __init__(self, name, symbol, pos, level, price):
        super().__init__(name, symbol, pos, level, price)
    @abstractmethod
    def use_effect(self, target):
        pass
    @abstractmethod
    def throw_effect(self, target):
        pass

class Equippable(Item):
    def __init__(self, name, symbol, pos, level, price, slots):
        super().__init__(name, symbol, pos, level, price)
        self.slot = slots
    @abstractmethod
    def on_equip(self, target):
        #code for checking if slot is filled
        pass
    @abstractmethod
    def on_unequip(self, target):
        #check if you have inventory space, if not, drop on the ground
        pass

class Weapon(Equippable):
    def __init__(self, name, symbol, pos, level, price, slots, type, range, damages, statuses):
        super().__init__(name, symbol, pos, level, price, slots)
        self.type = type
        self.range = range
        self.damages = damages
        self.statuses = statuses
    @abstractmethod
    def on_equip(self, target):
        super().on_equip(target)
    @abstractmethod
    def on_unequip(self, target):
        super().on_equip(target)

#When a two-handed weapon is equipped in a hand slot, this is placed in the other hand slot
class Unavailable(Equippable):
    def __init__(self, pos):
        super().__init__("", "", pos, 0, 0, ("right_hand", "left_hand"))
    def on_equip(self, target):
        super().on_equip(target)
    def on_unequip(self, target):
        super().on_unequip(target)

class Terrain(GameObject):
    def __init__(self, name, symbol, pos, hp, resistances, passable, blockSight, warn, warning):
        super().__init__(name, symbol, pos)
        self.hp = hp
        self.resistances = resistances
        self.dodge = 0
        self.passable = passable
        self.blockSight = blockSight
        #warn can be NO, YES, or WALK
        self.warn = warn
        #message displayed when warn is triggered
        self.warning = warning
    @abstractmethod
    def onCreation(self):
        pass
    #onStep applies every time a creature ends its turn on the tile with this terrain
    @abstractmethod
    def onStep(self, creature):
        pass

class Decor(GameObject):
    def __init__(self, name, symbol, pos, hp, resistances, passable, blockSight, warn, warning):
        super().__init__(name, symbol, pos)
        self.hp = hp
        self.resistances = resistances
        self.passable = passable
        self.blockSight = blockSight
        self.dodge = 0
        #warn can be NO, YES, or WALK
        self.warn = warn
        # message displayed when warn is triggered
        self.warning = warning
    @abstractmethod
    def onInteract(self, ceature):
        pass
    @abstractmethod
    def passiveBehavior(self):
        pass