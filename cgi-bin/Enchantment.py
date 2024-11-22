#!/usr/bin/python3
import random
import sys
import cgi
from GameObject import Weapon
from SubSystem import lookup_damage_type_id

#enchantment base class
class Enchantment():
    def __init__(self, name, level, price, damages, statuses):
        self.name = name
        self.level = level
        self.price = price
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

#function to pick a random enchantment
#item is the equippable item you want to generate an enchantment for
#depth is the current depth of the level
def random_enchantment(item_level, is_weapon, depth):
    if is_weapon:
        list = weapon_enchantments
    else:
        list = other_enchantments
    enchantment_level = choose_enchantment_level(item_level, depth)
    if enchantment_level <= 0:
        return None
    #find bounds for the enchantments of enchantment_level in the list
    start_index = -1
    end_index = -1
    for i in range(len(list)):
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

class Heat(Enchantment):
    def __init__(self,):
        super().__init__("Heat", 1, 30, [(lookup_damage_type_id("Fire"), 5, 2)], [])

class Fire(Enchantment):
    def __init__(self,):
        super().__init__("Flames", 2, 60, [(lookup_damage_type_id("Fire"), 10, 4)], [])

class Hellfire(Enchantment):
    def __init__(self,):
        super().__init__("Hellfire", 8, 240, [(lookup_damage_type_id("Fire"), 10, 4), (lookup_damage_type_id("Dark"), 10, 0)], [])

class Incineration(Enchantment):
    def __init__(self,):
        super().__init__("Incineration", 4, 120, [(lookup_damage_type_id("Fire"), 20, 6)], [])

class Sparking(Enchantment):
    def __init__(self,):
        super().__init__("Sparking", 3, 90, [(lookup_damage_type_id("Lightning"), 5, 2)], [])

class Lightning(Enchantment):
    def __init__(self,):
        super().__init__("Lightning", 6, 180, [(lookup_damage_type_id("Lightning"), 10, 2)], [])

class Electrocution(Enchantment):
    def __init__(self,):
        super().__init__("Electrocution", 12, 360, [(lookup_damage_type_id("Lightning"), 20, 4)], [])

class HolyLightning(Enchantment):
    def __init__(self,):
        super().__init__("Holy Lightning", 9, 270, [(lookup_damage_type_id("Lightning"), 10, 2), (lookup_damage_type_id("Light"), 5, 2)], [])

class Chilling(Enchantment):
    def __init__(self,):
        super().__init__("Chilling", 1, 30, [(lookup_damage_type_id("Cold"), 5, 0)], [])

class Cold(Enchantment):
    def __init__(self,):
        super().__init__("Cold", 2, 60, [(lookup_damage_type_id("Cold"), 10, 0)], [])

class Flux(Enchantment):
    def __init__(self,):
        super().__init__("Flux", 16, 480, [(lookup_damage_type_id("Fire"), 10, 4), (lookup_damage_type_id("Cold"), 10, 0)], [])

class Dissolving(Enchantment):
    def __init__(self,):
        super().__init__("Dissolving", 5, 150, [(lookup_damage_type_id("Acid"), 5, 2)], [])

class Melting(Enchantment):
    def __init__(self,):
        super().__init__("Melting", 10, 300, [(lookup_damage_type_id("Acid"), 10, 4)], [])

class Chaos(Enchantment):
    def __init__(self,):
        super().__init__("Chaos", 18, 540, [(lookup_damage_type_id("Acid"), 10, 4), (lookup_damage_type_id("Lightning"), 10, 2), (lookup_damage_type_id("Fire"), 10, 4)], [])

class Illumination(Enchantment):
    def __init__(self,):
        super().__init__("Illumination", 3, 90, [(lookup_damage_type_id("Light"), 5, 2)], [])

class Light(Enchantment):
    def __init__(self,):
        super().__init__("Light", 6, 180, [(lookup_damage_type_id("Light"), 10, 4)], [])

class Shadow(Enchantment):
    def __init__(self,):
        super().__init__("Shadow", 3, 90, [(lookup_damage_type_id("Dark"), 5, 0)], [])

class Darkness(Enchantment):
    def __init__(self,):
        super().__init__("Darkness", 6, 180, [(lookup_damage_type_id("Dark"), 10, 0)], [])

class Twilight(Enchantment):
    def __init__(self,):
        super().__init__("Twilight", 19, 570, [(lookup_damage_type_id("Light"), 10, 0), (lookup_damage_type_id("Dark"), 10, 0)], [])

class Decay(Enchantment):
    def __init__(self,):
        super().__init__("Decay", 5, 150, [(lookup_damage_type_id("Necrotic"), 5, 2)], [])

class Death(Enchantment):
    def __init__(self,):
        super().__init__("Death", 10, 300, [(lookup_damage_type_id("Necrotic"), 10, 4)], [])

class Undeath(Enchantment):
    def __init__(self,):
        super().__init__("Undeath", 15, 450, [(lookup_damage_type_id("Necrotic"), 15, 6)], [])

class Gravechill(Enchantment):
    def __init__(self,):
        super().__init__("Gravechill", 11, 330, [(lookup_damage_type_id("Necrotic"), 10, 4), (lookup_damage_type_id("Cold"), 5, 0)], [])

class Magic(Enchantment):
    def __init__(self,):
        super().__init__("Magic", 7, 210, [(lookup_damage_type_id("Arcane"), 5, 2)], [])

class Evil(Enchantment):
    def __init__(self,):
        super().__init__("Evil", 13, 390, [(lookup_damage_type_id("Dark"), 10, 0), (lookup_damage_type_id("Arcane"), 5, 2)], [])

class Wizardry(Enchantment):
    def __init__(self,):
        super().__init__("Wizardry", 14, 420, [(lookup_damage_type_id("Arcane"), 10, 4)], [])

class Fading(Enchantment):
    def __init__(self,):
        super().__init__("Fading", 10, 300, [(lookup_damage_type_id("Existence"), 5, 0)], [])

class Unraveling(Enchantment):
    def __init__(self,):
        super().__init__("Unraveling", 17, 300, [(lookup_damage_type_id("Existence"), 5, 0), (lookup_damage_type_id("Arcane"), 5, 2)], [])

class Annihilation(Enchantment):
    def __init__(self,):
        super().__init__("Annihilation", 20, 600, [(lookup_damage_type_id("Existence"), 10, 0)], [])


#enchantments list ordered from highest level to lowest level
weapon_enchantments = [Heat(), Chilling(), Fire(), Sparking(), Illumination(), Shadow(), Incineration(), Dissolving(), Decay(), Lightning(), Light(), Darkness(), Magic(), Hellfire(), HolyLightning(), Melting(), Death(), Fading(), Gravechill(), Electrocution(), Evil(), Wizardry(), Undeath(), Flux(), Unraveling(), Chaos(), Twilight(), Annihilation()]
other_enchantments = []


#utility function to pick the enchantment's level:
def choose_enchantment_level(item_level, depth):
    enchantment_level = depth - item_level
    chance = 0.1
    while enchantment_level > 0:
        roll = random.random()
        if roll > chance:
            chance += 0.1
            enchantment_level -= 1
            continue
        else:
            break
    return enchantment_level
