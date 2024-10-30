#!/usr/bin/python3
import sys
import cgi
from GameObject import Item, Consumable, Equippable, Weapon, Unavailable, LightSourceItem
from SubSystem import lookup_damage_type_id, lookup_skill_id
from ActiveAbilities import Spell, Technique, HealingTouch


class Pebble(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Pebble", "17", pos, amount, 16, 1, 0)
    #TODO: implement as ammo for slings

class LesserHealth(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Lesser Health Potion", "17", pos, amount, 16, 1, 0)
    def use_effect(self, grid, target):
        target.heal(int(target.max_hp*0.1))

class MedHealth(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Health Potion", "17", pos, amount, 16, 1, 0)
    def use_effect(self, grid, target):
        target.heal(int(target.max_hp*0.25))

class GreaterHealth(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Greater Health Potion", "17", pos, amount, 16, 1, 0)
    def use_effect(self, grid, target):
        target.heal(int(target.max_hp*0.5))

class Ore(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Ore", "17", pos, amount, 10, 1, 10)

class Corruptite(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Corruptite Dust", "17", pos, amount, 5, 3, 20)
    #TODO: implement buffs and addiction


class IronDagger(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Dagger", "17", pos, 1, 5, 1, "One-Handed Blade", 1, 3,
                         [(lookup_damage_type_id("Piercing"), 3, 1)], [], ("Right Hand", "Left Hand"), enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class WoodenClub(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Wooden Club", "17", pos, 1, 1, 1, "One-Handed Mace", 1, 1.5,
                         [(lookup_damage_type_id("Blunt"), 5, 0)], [], ("Right Hand", "Left Hand"), enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class LeatherCuirass(Equippable):
    def __init__(self, pos, level):
        super().__init__("Leather Cuirass", "17", pos, level, 15, 10, "Torso")
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.resistances[lookup_damage_type_id("PRC")] += 0.025
        equipped_creature.resistances[lookup_damage_type_id("SLH")] += 0.05
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        equipped_creature.resistances[lookup_damage_type_id("PRC")] -= 0.025
        equipped_creature.resistances[lookup_damage_type_id("PRC")] -= 0.05

class HealingTouchScroll(Consumable):
    def __init__(self, pos):
        super().__init__("Scroll of Healing Touch", "1", pos, 1, 1, 3, 300)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(HealingTouch())