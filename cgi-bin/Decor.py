#!/usr/bin/python3
import copy
import random
import sys
import cgi
from GameObject import Decor, LightDecor, spread_light, Gold
from Level import Level, Biome
from Biomes import TempBiome
from Items import *
from Creatures import Ghost

class Corpse(Decor):
    def __init__(self, pos, hp, resistances):
        super().__init__("Corpse", "34", pos, hp, resistances, True, False, "NO", "")


class Stairs(Decor):
    def __init__(self, pos):
        super().__init__("Stairs", "23", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "Yes", "Go Down?")
    def on_interact(self, current_level, creature):
        pass

#used for the ziggurat>carrion level transition, as well as for the oldtemple>cosmicvoid and cosmicvoid>worldheart
class Portal(Decor):
    def __init__(self, pos):
        super().__init__("Portal", "15", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, False, "Yes", "Go Down?")
    def on_interact(self, current_level, creature):
        pass

#mine, corruptite mine, shantytown, undercity
class Door(Decor):
    def __init__(self, pos):
        super().__init__("Wooden Door", '24', pos, 40, (0.7, 0.7, 0.3, -1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_interact(self, grid, creature):
        self.block_sight = self.passable
        self.passable = not self.passable
        self.textureIndex = 35 if self.passable else 24
        

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
        super().__init__("Rock", "56", pos, 70, (0.7, 0.9, 1.0, 1.0, 0.7, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), True, True, "NO", "")
    def on_destroy(self, grid):
        grid[self.pos[0]][self.pos[1]].append(Pebble(self.pos, 10))
        super().on_destroy(grid)

#cove: uncommon
class Coral(Decor):
    def __init__(self, pos):
        super().__init__("Coral", "55", pos, 40, (0.7, 0.9, 0.2, 1.0, 1.0, 1.0, 1.0, 0.1, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")

# mines, corruptite mines: uncommon
class Deposit(Decor):
    def __init__(self, pos):
        super().__init__("Mineral Deposit", "46", pos, 70, (0.7, 0.9, 1.0, 1.0, 0.7, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_destroy(self, grid):
        grid[self.pos[0]][self.pos[1]].append(Ore(self.pos, 5))
        super().on_destroy(grid)

#corruptite mines: rare
class CorruptiteCluster(Decor):
    def __init__(self, pos):
        super().__init__("Corruptite Cluster", "48", pos, 40, (0.7, 0.9, 0.2, 1.0, 1.0, 1.0, 1.0, 0.1, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_destroy(self, grid):
        grid[self.pos[0]][self.pos[1]].append(Corruptite(self.pos, 3))
        super().on_destroy(grid)

#columbarium: common
#catacombs: uncommon
class Urn(Decor):
    def __init__(self, pos):
        super().__init__("Burial Urn", "49", pos, 10, (0.0, 0.5, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0), False, True, "NO", "")
    def on_destroy(self, grid):
        grid[self.pos[0]][self.pos[1]].append(Ghost(self.pos))
        super().on_destroy(grid)

#mine, corruptite mine, sewer, shantytown, ziggurat: common
class StandingTorch(LightDecor):
    def __init__(self, pos):
        super().__init__( "Torch", "50", pos, 5, (0.7, 0.7, 0.3, -1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0), True, "NO", "", .7, True)

#embers: common
class Ember(LightDecor):
    def __init__(self, pos):
        super().__init__( "Ember", "51", pos, 5, (0.7, 0.9, 1.0, 1.0, 0.7, 0.0, -1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0), False, "NO", "", .6, True)

#carrion, worldeater's gut: common
class LightGrowth(LightDecor):
    def __init__(self, pos):
        super().__init__( "Growth", "52", pos, 60, (0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0), False, "NO", "", .7, True)


#columbarium, catacombs, necropolis: common
class SpiritLight(LightDecor):
    def __init__(self, pos):
        super().__init__( "Spirit Light", "53", pos, 5, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0), True, "NO", "", .6, True)

#cosmic void: common
class Energy(LightDecor):
    def __init__(self, pos):
        super().__init__( "Energy", "54", pos, 200, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0), True, "NO", "", 1, True)

levelzero_dialogue = ["Are you sure you want to enter the caverns?"]
cave_dialogue = ["Hi"]
cove_dialogue = ["Hi"]
mine_dialogue = ["Hi"]
corruptmine_dialogue = ["Hi"]
sewer_dialogue = ["Hi"]
shantytown_dialogue = ["Hi"]
magmacore_dialogue = ["It's really hot in here"]
deepcavern_dialogue = ["Hi"]
ziggurat_dialogue = ["sssh, be quiet, I'm not exactly welcome here"]
catacomb_dialogue = ["Hi"]
carrion_dialogue = ["Hi"]
worldeatersgut_dialogue = ["I hardly get any business", "I don't know why I thought it was a good idea to set up shop in the belly of a new god"]
necropolis_dialogue = ["I'm dead but I still love gold"]

class Shop(Decor):
    def __init__(self, name, pos, inventory, dialogue):
        super().__init__(name, "47", pos, 1, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), False, False, "NO", "")
        self.inventory = inventory
        self.dialogue = dialogue
    def on_interact(self, grid, creature):
        pass
        #TODO: show shop UI
    def buy(self, grid, buyer, item):
        buyer_gold = None
        buyer_purchase = None
        for buyer_item in buyer.inventory:
            if isinstance(buyer_item, Gold):
                buyer_gold = buyer_item
            if buyer_item == item:
                buyer_purchase = buyer_item
        if buyer_gold is None or buyer_gold.amount < item.price:
            return False
        shop_gold = None
        for shop_item in self.inventory:
            if isinstance(shop_item, Gold):
                shop_gold = shop_item
        buyer_gold.amount -= item.price
        if shop_gold is None:
            self.inventory.append(Gold((-1, -1), item.price))
        else:
            shop_gold.amount += item.price
        if buyer_purchase is None:
            original_amount = item.amount
            item.amount = 1
            buyer.inventory.append(copy.copy(item))
            item.amount = original_amount
        else:
            buyer_purchase.amount += 1
        item.amount -= 1
        if item.amount == 0:
            self.inventory.remove(item)
    def sell(self, grid, buyer, item):
        buyer_gold = None
        for buyer_item in buyer.inventory:
            if isinstance(buyer_item, Gold):
                buyer_gold = buyer_item
            if buyer_item == item:
                buyer_purchase = buyer_item
        shop_gold = None
        shop_purchase = None
        for shop_item in self.inventory:
            if isinstance(shop_item, Gold):
                shop_gold = shop_item
            if shop_item == item:
                shop_purchase = shop_item
        if shop_gold is None or shop_gold.amount < item.price:
            return False
        shop_gold.amount -= item.price
        if buyer_gold is None:
            self.inventory.append(Gold((-1, -1), item.price//4))
        else:
            buyer_gold.amount += item.price//4
        if shop_purchase is None:
            original_amount = item.amount
            item.amount = 1
            self.inventory.append(copy.copy(item))
            item.amount = original_amount
        else:
            shop_purchase.amount += 1
        item.amount -= 1
        if item.amount == 0:
            buyer.inventory.remove(item)
    def talk(self):
        return self.dialogue[random.randint(0, len(self.dialogue))]

class RandomShop(Shop):
    def __init__(self, name, pos, depth, dialogue):
        inventory = [Gold((-1, -1), 100)]
        for i in range(10):
            inventory.append(random_item((-1, -1), depth))
        super().__init__(name, pos, inventory, dialogue)

class LevelZeroWeaponShop(Shop):
    def __init__(self, pos):
        inventory = [IronDagger((-1, -1), None), IronShortsword((-1, -1), None), IronGreatsword((-1, -1), None), IronHatchet((-1, -1), None), IronGreataxe((-1, -1), None), WoodenClub((-1, -1), None), WoodenGreatclub((-1, -1), None), IronSpear((-1, -1), None), IronHalberd((-1, -1), None), Sling((-1, -1), None), OakShortbow((-1, -1), None), OakLongbow((-1, -1), None), Pebble((-1, -1), 16), Arrow((-1, -1), 16)]
        super().__init__("Weapon Shop", pos, inventory, levelzero_dialogue)
        self.hp = "Weapons"

class LevelZeroArmorShop(Shop):
    def __init__(self, pos):
        inventory = [WoodenBuckler((-1, -1), None), LeatherSkullcap((-1, -1), None), LeatherCuirass((-1, -1), None), LeatherBoots((-1, -1), None),]
        super().__init__("Armor Shop", pos, inventory, levelzero_dialogue)
        self.hp = "Armor"

class LevelZeroScrollShop(Shop):
    def __init__(self, pos):
        inventory = [FireBoltScroll((-1, -1), 1), IceBoltScroll((-1, -1), 1)]
        super().__init__("Scroll Shop", pos, inventory, levelzero_dialogue)
        self.hp = "Scrolls"
