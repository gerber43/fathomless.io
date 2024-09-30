from abc import abstractmethod
import random
from operator import truediv

from Subsystem import StatusEffect, lookup_crit_status_effect


class GameObject:
    def __init__(self, name, symbol, pos):
        self.name = name
        self.symbol = symbol
        self.pos = pos
    def move(self, newPos):
        if ((isinstance(self, Item)) and (newPos == -1)):
            fakevar = 1
            #player.addToInventory(self)
        self.pos = newPos

class Item(GameObject):
    def __init__(self, name, symbol, pos, level, price):
        super().__init__(name, symbol, pos)
        #The item's level is a general guide for how powerful it should be
        self.level = level
        #Price the item will be sold for in shops
        self.price = price

class Creature(GameObject):
    def __init__(self, name, symbol, pos, segments, hp, mp, status_effects, fitness, cunning, magic, accuracy, dodge, critChance, equipment, skills, abilities, damage_resistances, status_resistances, dropTable):
        super().__init__(name, symbol, pos)
        #list of creature segments, should be empty for single-tile creatures
        self.segments = segments
        self.hp = hp
        self.mp = mp
        self.status_effects = status_effects
        self.fitness = fitness
        self.cunning = cunning
        self.magic = magic
        self.accuracy = accuracy
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
        self.status_effects.append(type_id, stacks, infinite)

    def basicAttack(self, target):
        #TODO: Implement ammo checking and ammo decrement
        if isinstance(target, CreatureSegment):
            target = target.creature
        hitChance = self.accuracy - target.dodge
        hitRoll = random.random
        if hitRoll > hitChance:
            return
        critRoll = random.random
        crit = True
        if critRoll > self.critChance:
            crit = False
        for damage in self.equipment.weapon.damages:
            total = damage.base
            if crit:
                total = total*self.equipment.weapon.critMult
            else:
                total = total + random.randint(-damage.var, damage.var)
            if (damage.dmgtype == 0) or (damage.dmgtype == 1) or (damage.dmgtype == 2):
                total = total + self.fitness
            total = total * (1-target.damage_resistances[damage.dmgtype])
            target.hp -= total
            if crit:
                target.gainStatusEffect(lookup_crit_status_effect(damage.dmgtype), total/10, False)
        for status in self.equipment.weapon.statuses:
            target.gainStatusEffect(status.type_id, status.stacks, status.infinite)

#support multi-tile creatures
class CreatureSegment(GameObject):
    def __init__(self, creature, symbol, pos):
        super().__init__(creature.name, symbol, pos)
        self.creature = creature

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