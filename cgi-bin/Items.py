#!/usr/bin/python3
import random
import sys
import cgi
from GameObject import Item, Consumable, Equippable, Weapon, TwoHandedWeapon, LightSourceItem
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



#player-usable items
class Pebble(Item):
    def __init__(self, pos, amount):
        super().__init__("Pebble", "17", pos, amount, 16, 1, 0)
class Arrow(Item):
    def __init__(self, pos, amount):
        super().__init__("Arrow", "17", pos, amount, 16, 2, 5)

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

class LesserMana(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Lesser Mana Potion", "40", pos, amount, 4, 2, 20)
    def use_effect(self, grid, target):
        target.mp += int(target.max_mp*0.1)

class MedMana(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Mana Potion", "40", pos, amount, 4, 7, 80)
    def use_effect(self, grid, target):
        target.mp += int(target.max_mp*0.25)

class GreaterMana(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Greater Mana Potion", "40", pos, amount, 4, 15, 150)
    def use_effect(self, grid, target):
        target.mp += int(target.max_mp*0.5)

class Bandage(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Bandage", "40", pos, amount, 16, 15, 5)
    def use_effect(self, grid, target):
        target.heal(0)

class Antidote(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Antidote", "40", pos, amount, 16, 15, 20)
    def use_effect(self, grid, target):
        for status in target.status_effects:
            if status.status_type == "Poison":
                target.status_effects.remove(status)
                break

class Ore(Item):
    def __init__(self, pos, amount):
        super().__init__("Ore", "17", pos, amount, 10, 1, 10)

class Corruptite(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Corruptite Dust", "17", pos, amount, 5, 3, 20)
    #TODO: implement buffs and addiction

class Amulet(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Amulet", "17", pos, 0, 0, 1, "Neck", enchantment)

class Ring(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Amulet", "17", pos, 1, 15, 1, "Fingers", enchantment)

#tier 1 weapons

class IronDagger(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Dagger", "17", pos, 1, 5, 1, "One-Handed Blade", 1, 3,
                         [(lookup_damage_type_id("Piercing"), 3, 1)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class IronShortsword(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Shortsword", "17", pos, 1, 10, 3, "One-Handed Blade", 1, 1.5,
                         [(lookup_damage_type_id("Slashing"), 5, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class IronGreatsword(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Greatsword", "17", pos, 1, 30, 10, "Two-Handed Blade", 1, 2,
                         [(lookup_damage_type_id("Slashing"), 10, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class IronHatchet(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Hatchet", "17", pos, 1, 10, 5, "One-Handed Axe", 1, 1.75,
                         [(lookup_damage_type_id("Slashing"), 5, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class IronGreataxe(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Greataxe", "17", pos, 1, 30, 15, "Two-Handed Axe", 1, 2.25,
                         [(lookup_damage_type_id("Slashing"), 10, 8)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class WoodenClub(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Wooden Club", "17", pos, 1, 1, 15, "One-Handed Mace", 1, 1.5,
                         [(lookup_damage_type_id("Blunt"), 5, 0)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class WoodenGreatclub(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Wooden Club", "17", pos, 1, 1, 20, "Two-Handed Mace", 1, 1.25,
                         [(lookup_damage_type_id("Blunt"), 10, 0)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class IronSpear(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Spear", "17", pos, 1, 15, 5, "Polearm", 2, 1.25,
                         [(lookup_damage_type_id("Piercing"), 3, 1)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class IronHalberd(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Halberd", "17", pos, 1, 30, 15, "Polearm", 2, 1.25,
                         [(lookup_damage_type_id("Piercing"), 5, 1), (lookup_damage_type_id("Slashing"), 5, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class Sling(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Sling", "17", pos, 1, 15, 5, "Sling", 5, 1.5,
                         [(lookup_damage_type_id("Blunt"), 3, 1)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class OakShortbow(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Oak Shortbow", "17", pos, 1, 15, 3, "Bow", 5, 2,
                         [(lookup_damage_type_id("Piercing"), 5, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class OakLongbow(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Oak Longbow", "17", pos, 1, 30, 7, "Bow", 9, 2,
                         [(lookup_damage_type_id("Piercing"), 5, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

#level 1 armor

class WoodenBuckler(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Wooden Buckler", "42", pos, 1, 5, 7, "Hands", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.02
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.04

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.02
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.04

#level 2 armor

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

#scrolls

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
