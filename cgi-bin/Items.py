#!/usr/bin/python3
import random
import sys
import cgi
from GameObject import Item, Consumable, Equippable, Weapon, Unavailable, LightSourceItem
from SubSystem import lookup_damage_type_id, lookup_skill_id
from ActiveAbilities import Spell, Technique, HealingTouch
from Enchantment import random_enchantment

#list of spawnable items, the name, their level, and their type
items = [("Amulet", 0, "Equipment"), ("Ring", 1, "Equipment"), ("IronDagger", 1, "Weapon"), ("IronSpear", 1, "Weapon"), ("WoodenClub", 1, "Weapon"), ("LeatherCuirass", 2, "Equipment"), ("LesserHealth", 2, "Consumable"), ("HealingTouchScroll", 3, "Consumable"), ("MedHealth", 7, "Consumable"), ("GreaterHealth", 15, "Consumable")]

#function to pick a random item
def random_item(pos, depth):
    global items
    end_index = -1
    for i in range(len(items)):
        if items[i][1] > depth:
            end_index = i - 1
            break
    if end_index == -1:
        end_index = len(items)
    item = items[random.randint(0, end_index - 1)]
    if item[2] == "Consumable":
        return eval(item[0])(pos, depth//item[1])
    if item[2] == "Weapon":
        #return eval(item[0])(pos, random_enchantment(item[1], True, depth))
        return eval(item[0])(pos, None)

    #TODO: Create at least 21 non-weapon enchantments and re-enable this code
    #return eval(item[0])(pos, random_enchantment(item[1], False, depth))
    return eval(item[0])(pos, None)



#items
class Pebble(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Pebble", "17", pos, amount, 16, 1, 0)
    #TODO: implement as ammo for slings

class LesserHealth(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Lesser Health Potion", "40", pos, amount, 4, 2, 20)
    def use_effect(self, grid, target):
        target.heal(target.max_hp*0.1)

class MedHealth(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Health Potion", "40", pos, amount, 4, 7, 80)
    def use_effect(self, grid, target):
        target.heal(target.max_hp*0.25)

class GreaterHealth(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Greater Health Potion", "40", pos, amount, 4, 15, 150)
    def use_effect(self, grid, target):
        target.heal(target.max_hp*0.5)

class Bandage(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Bandage", "40", pos, amount, 16, 15, 5)
    def use_effect(self, grid, target):
        target.heal(0)

class Ore(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Ore", "17", pos, amount, 10, 1, 10)

class Corruptite(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Corruptite Dust", "17", pos, amount, 5, 3, 20)
    #TODO: implement buffs and addiction

class Amulet(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Amulet", "17", pos, 0, 0, 1, ("Neck"), enchantment)

class Ring(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Amulet", "17", pos, 1, 15, 1, ("Neck"), enchantment)

class IronDagger(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Dagger", "17", pos, 1, 5, 1, "One-Handed Blade", 3, 3,
                         [(lookup_damage_type_id("Piercing"), 3, 1)], [], ("Right Hand", "Left Hand"), enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class IronSpear(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Spear", "17", pos, 1, 15, 5, "Polearm", 2, 1.25,
                         [(lookup_damage_type_id("Piercing"), 3, 1)], [], ("Right Hand", "Left Hand"), enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class WoodenClub(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Wooden Club", "17", pos, 1, 1, 10, "One-Handed Mace", 1, 1.5,
                         [(lookup_damage_type_id("Blunt"), 5, 0)], [], ("Right Hand", "Left Hand"), enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class LeatherCuirass(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Leather Cuirass", "42", pos, 2, 15, 10, "Torso", enchantment)
    def on_equip(self, grid, equipped_creature):
        
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.025
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.05
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.025
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.05

class HealingTouchScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Healing Touch", "41", pos, amount, 1, 3, 300)
    def use_effect(self, grid, target):
        target.abilities.append(HealingTouch())
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(HealingTouch())
