#!/usr/bin/python3
import random
import sys
import cgi
from GameObject import Weapon

#enchantment base class
class Enchantment():
    def __init__(self, name, level, damages, statuses):
        self.name = name
        self.level = level
        self.damages = damages
        self.statuses = statuses
    def on_equip(self, grid, equipped_creature):
        pass
    def on_unequip(self, grid, equipped_creature):
        pass
    def on_move(self, grid, equipped_creature, new_pos):
        pass
    def on_attack(self, grid, equipped_creature, target):
        pass
    def on_attacked(self, grid, equipped_creature, attacker):
        pass
    def on_ability(self, grid, equipped_creature, target):
        pass

#enchantments list ordered from highest level to lowest level
weapon_enchantments = []
other_enchantments = []


#utility function to pick the enchantment's level:
def choose_enchantment_level(item_level, depth):
    enchantment_level = depth - item_level
    chance = 0.1
    while enchantment_level > 0:
        roll = random.random
        if roll > chance:
            chance += 0.1
            continue
        else:
            break
    return enchantment_level

#function to pick a random enchantment
#item is the equippable item you want to generate an enchantment for
#depth is the current depth of the level
def random_enchantment(item, depth):
    if isinstance(item, Weapon):
        list = weapon_enchantments
    else:
        list = other_enchantments
    enchantment_level = choose_enchantment_level(item.level, depth)
    start_index = -1
    end_index = -1
    for i in range(list):
        if list[i].level == enchantment_level:
            if start_index == -1:
                start_index = i
        elif start_index != -1:
            end_index = i - 1
            break
    if end_index == -1:
        end_index = len(list) - 1
    return list[random.randint(start_index, end_index)]





#weapon enchantment definitions

#other enchantment definitions