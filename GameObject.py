from abc import abstractmethod
import random
from operator import truediv


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
    def __init__(self, name, symbol, pos, hp, mp, fitness, cunning, magic, accuracy, dodge, critChance, equipment, skills, abilities, resistances, dropTable):
        super().__init__(name, symbol, pos)
        self.hp = hp
        self.mp = mp
        self.fitness = fitness
        self.cunning = cunning
        self.magic = magic
        self.accuracy = accuracy
        self.dodge = dodge
        self.critChance = critChance
        self.equipment = equipment
        self.skills = skills
        self.abilities = abilities
        self.resistances = resistances
        self.dropTable = dropTable
    def basicAttack(self, target):
        #TODO: Implement range checking and cancel attack and return to player input if target isn't in range
        #TODO: Implement ammo checking and ammo decremenmt
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
            if (crit):
                total = total*self.equipment.weapon.critMult
            else:
                total = total + random.randint(-damage.var, damage.var)
            if (damage.type == "PRC") or (damage.type == "SLH") or (damage.type == "BLT"):
                total = total + self.fitness
            total = total * (1-target.resistances.getResistance(damage.type))
            target.hp -= total

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