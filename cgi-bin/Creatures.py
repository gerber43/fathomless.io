#!/usr/bin/python3
import sys
import cgi
import random
from asyncio import start_unix_server

from GameObject import Creature, CreatureSegment, Boss, Gold, Unavailable
from Items import *
from StatusEffects import Poison, Flight, Regeneration, Burning, Suffocation
from ActiveAbilities import *
from Enchantment import *
from Terrain import Wall

#Piercing, Slashing, Blunt, Fire, Lightning, Water, Cold, Acid, Light, Dark, Necrotic, Arcane, Existence
basicDamageResistances = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
#Bleed, Stun, Burning, Suffocation, Frozen, Blindness, Rot, Manaburn, Nonexistence, Poison, Fear, Confusion, Mindbreak, Midas Curse, Bloodsiphon, Manadrain, Death
basicStatusResistances = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#One-Handed Blades, One-Handed Axes, One-Handed Maces, Two-Handed Blades, Two-Handed Axes, Two-Handed Maces, Polearms, Slings, Bows, Elementalism, Cursing, Enhancement, Transmutation, Summoning, Dual-Wielding, Memory, Search, Hide, Lockpicking, Disarm Trap
#Right Hand, Left Hand, Head, Torso, Legs, Feet, Hands, Neck, Right Finger, Left Finger

# cave
class Goblin(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Goblin", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 4, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

#cave
class Bandit(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronShortsword((-1, -1), None)
        else:
            weapon = IronHatchet((-1, -1), None)
        shield_choice = random.randint(0, 4)
        if shield_choice == 4:
            shield = WoodenBuckler((-1, -1), None)
        else:
            shield = None
        super().__init__("Bandit", "22", pos, [], 20, 0, 1, [], 3, 3, 0, 3, 0.25, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 3, 0),
                         (weapon, shield, None, LeatherCuirass((-1, -1), None), None, LeatherBoots((-1, -1), None), None, None, None), [],
                         (0.025, 0.05, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 5), 0.7)), 20, 2)
        if shield is not None:
            self.damage_resistances[0] += 0.02
            self.damage_resistances[0] += 0.04

#cave
class Ogre(Creature):
    def __init__(self, pos):
        super().__init__("Ogre", "22", pos, [CreatureSegment(self, "22", (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, "22", (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, "22", (pos[0] + 1, pos[1] + 1), "Static")], 50, 0, 1, [], 7, 0, 0, 0, 0.05, 10,
                         (0, 0, 5, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (WoodenGreatclub((-1, -1), None), None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, [], 50, 3)

class SpiderFangs(Weapon):
    def __init__(self):
        super().__init__("Fang", "17", (-1, -1), 0, 0, 0, "One-Handed Blade", 1, 1.5,
                         [(lookup_damage_type_id("Piercing"), 3, 1)], [Poison(3, False)], None)

# cave
class Spider(Creature):
    def __init__(self, pos):
        super().__init__("Spider", "26", pos, [], 10, 0, 1, [], 1, 3, 0, 4, 0.05, 20,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (SpiderFangs(), None, None, None, None, None, None, None, None), [], (0.3, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.6, 0.0, 0.0),
                         (0.5, 0.0, 0.0, 0.0, 0.3, 0.6, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0), [], 0, ((MinorPoison((-1, -1), 1), 0.3)), 10, 1)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 5, False, target):
                self.basic_attack_damage(grid, SpiderFangs(), target, self.crit_check(grid))

class BatFangs(Weapon):
    def __init__(self):
        super().__init__("Fang", "17", (-1, -1), 0, 0, 0, "One-Handed Blade", 1, 1.2,
                         [(lookup_damage_type_id("Piercing"), 1, 0)], [Bleed(2, False)], None)

# cave and deep cavern
class Bat(Creature):
    def __init__(self, pos):
        super().__init__("Bat", "27", pos, [], 5, 0, 1, [Flight(1, True)], 1, 3, 0, 5, 0.05, 30,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (BatFangs(), None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0), [], 0, [], 5, 1)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 3, False, target):
            self.basic_attack_damage(grid, SpiderFangs(), target, self.crit_check(grid))

# cove
class Fishman(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronShortsword((-1, -1), None)
        else:
            weapon = IronSpear((-1, -1), None)
        super().__init__("Deep One", "28", pos, [], 30, 0, 1, [], 3, 3, 0, 2, 0.1, 7,
                         (5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),
                         (weapon, None, None, None, None, None, None, None, None), [], (0.2, 0.5, 0.0, -0.5, -0.2, 2.0, 0.9, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0),
                         (0.9, 0.0, -0.5, 1.0, 0.9, 0.5, 0.0, 0.0, 0.0, 0.3, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0), [], 0, ((Gold((-1, -1), 7), 0.7)), 30, 3)

# cove
class FishmanShaman(Creature):
    def __init__(self, pos):
        super().__init__("Deep One Shaman", "22", pos, [], 25, 50, 1, [], 0, 3, 5, 2, 0.05, 10,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 2, 0),
                         (WoodenClub((-1, -1), None), None, None, None, None, None, None, None, None), [IceBolt(), ChokingDeep()], (0.2, 0.5, 0.0, -0.5, -0.2, 2.0, 0.9, 0.0, 1.0, 0.5, 0.0, 0.3, 0.0),
                         (0.9, 0.0, -0.5, 1.0, 0.9, 0.5, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), [LesserMana((-1, -1), 4)], 1, [[Gold((-1, -1), 7), 0.7], [LesserMana((-1, -1), 1), 0.2]], 40, 4)

class CrusherClaw(Weapon):
    def __init__(self):
        super().__init__("Crusher Claw", "17", (-1, -1), 0, 0, 0, "One-Handed Blade", 1, 2,
                         [(lookup_damage_type_id("Blunt"), 15, 4)], [], None)
class PincerClaw(Weapon):
    def __init__(self):
        super().__init__("Pincer Claw", "17", (-1, -1), 0, 0, 0, "One-Handed Blade", 1, 1.25,
                         [(lookup_damage_type_id("Piercing"), 5, 2)], [Bleed(3, False)], None)
# cove
class GiantCrab(Creature):
    def __init__(self, pos):
        super().__init__("Bloodclaw", "10", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 100, 0, 1, [], 7, 2, 0, 1, 0.2, 10,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (CrusherClaw(), PincerClaw(), None, None, None, None, None, None, None), [], (0.7, 0.7, 0.7, 0.0, 0.0, 1.0, 0.5, 0.0, 1.0, 0.0, 0.3, 0.0, 0.0),
                         (0.9, 0.5, 0.0, 0.7, 0.3, 0.0, 0.0, 0.0, 0.0, 0.4, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0), [], 0, [], 100, 6)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 3, False, target):
            self.basic_attack_damage(grid, CrusherClaw(), target, self.crit_check(grid))
        if self.basic_attack_hit_check(grid, 5, False, target):
            self.basic_attack_damage(grid, PincerClaw(), target, self.crit_check(grid))


# cove
class Pirate(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon_one = IronShortsword((-1, -1), None)
            weapon_two = IronShortsword((-1, -1), None)
            inventory = []
            inventory_size = 0
            drop_table = ((Gold((-1, -1), 50), 0.4))
        else:
            weapon_one = OakShortbow((-1, -1), None)
            weapon_two = Unavailable()
            inventory = [Arrow((-1, -1), 16), Arrow((-1, -1), 16), Arrow((-1, -1), 16), Arrow((-1, -1), 16)]
            inventory_size = 4
            drop_table = ((Gold((-1, -1), 20), 0.4), (Arrow((-1, -1), 4), 0.5))
        super().__init__("Pirate", "29", pos, [], 30, 0, 1, [], 3, 5, 0, 7, 0.5, 10,
                         (10, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 5, 0),
                         (weapon_one, weapon_two, None, None, None, LeatherBoots((-1, -1), None), None, None, None), [], (0.01, 0.02, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
                         basicStatusResistances, inventory, inventory_size, drop_table, 30, 3)

class DrownedAttack(Weapon):
    def __init__(self):
        super().__init__("", "17", (-1, -1), 0, 0, 0, "One-Handed Mace", 1, 3,
                         [(lookup_damage_type_id("Blunt"), 3, 0)], [], None)
# cove
class Drowned(Creature):
    def __init__(self, pos):
        super().__init__("Drowned", "22", pos, [], 100, 0, 1, [], 10, 0, 0, 1, 0.05, 10,
                         (3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
                         (DrownedAttack(), None, None, None, None, None, None, None, None), [], (0.0, 0.0, 0.0, -0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, -0.5),
                         (1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, -0.25, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0), [], 0, (), 20, 2)

# cove
class DrownedSailor(Creature):
    def __init__(self, pos):
        super().__init__("Drowned Sailor", "22", pos, [], 100, 0, 1, [], 10, 0, 0, 1, 0.05, 10,
                         (3, 3, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
                         (IronHatchet([-1, -1], None), None, None, None, None, LeatherBoots([-1, -1], None), None, None, None), [], (0.0, 0.0, 0.0, -0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, -0.5),
                         (1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, -0.25, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0), [], 0, [[Gold([-1, -1], 20), 0.3]], 25, 2)


# cove
class DrownedPirate(Creature):
    def __init__(self, pos):
        super().__init__("Drowned Pirate", "22", pos, [], 100, 0, 1, [], 10, 0, 0, 1, 0.05, 10,
                         (3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 0),
                         (IronShortsword([-1, -1], None), IronShortsword([-1, -1], None), None, None, None, LeatherBoots([-1, -1], None), None, None, None), [], (0.01, 0.02, 0.0, -0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, -0.5),
                         (1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, -0.25, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0), [], 0, [[Gold([-1, -1], 50), 0.4]], 40, 3)


# boss in cove 2
class DrownedCaptain(Boss):
    def __init__(self, pos):
        super().__init__("Drowned Captain", "31", pos, [], 150, 100, 1, [], 15, 5, 10, 10, 0.25,
                         (SteelShortsword([-1, -1], Chilling()), SteelShortsword([-1, -1], Decay()), None, None, None, LeatherBoots([-1, -1], None), None, None, None),
                         (15, 15, 0, 0, 0, 0, 0, 0, 0, 10, 10, 0, 0, 0, 0, 0, 10, 0, 2, 0, 5, 0), [ChokingDeep(), TidalWave()],
                         (0.01, 0.02, 0.0, -0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, -0.5),
                         (1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, -0.25, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0), [], 0, [SteelShortsword([-1, -1], Chilling()), SteelShortsword([-1, -1], Decay()), CreateWaterScroll()], 200, 10)

class IronPickaxe(Weapon):
    def __init__(self, pos):
        super().__init__("Iron Pickaxe", "17", pos, 1, 0, 0, "One-Handed Axe", 1, 2,
                         [[lookup_damage_type_id("Piercing"), 5, 1]], [], None)

# Mine and Corruptite Mine
class GoblinMiner(Creature):
    def __init__(self, pos):
        super().__init__("Goblin Miner", "32", pos, [], 10, 0, 1, [], 1, 5, 0, 4, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (IronPickaxe([-1, -1]), None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, [[Gold([-1, -1], 7), 0.7], [IronPickaxe([-1, -1]), 0.1]], 15, 1)

class GoblinMinerAddict(Creature):
    def __init__(self, pos):
        super().__init__("Goblin Miner", "32", pos, [], 10, 0, 1, [], 1, 5, 0, 4, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (IronPickaxe([-1, -1]), None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [Corruptite([-1, -1], 5)], 1, [[Gold([-1, -1], 7), 0.7], [IronPickaxe([-1, -1]), 0.1], [Corruptite([-1, -1], 2)], 0.2], 15, 1)

class SteelPickaxe(Weapon):
    def __init__(self, pos):
        super().__init__("Steel Pickaxe", "17", pos, 1, 0, 0, "One-Handed Axe", 1, 2,
                         [[lookup_damage_type_id("Piercing"), 10, 1]], [], None)

# Mine and Corruptite Mine
class HobgoblinMiner(Creature):
    def __init__(self, pos):
        super().__init__("Hobgoblin Miner", "22", pos, [], 30, 0, 1, [], 3, 5, 0, 4, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (SteelPickaxe([-1, -1]), None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, [[Gold([-1, -1], 12), 0.7], [SteelPickaxe([-1, -1]), 0.1]], 45, 3)

class HobgoblinMinerAddict(Creature):
    def __init__(self, pos):
        super().__init__("Hobgoblin Miner", "22", pos, [], 30, 0, 1, [], 3, 5, 0, 4, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (SteelPickaxe([-1, -1]), None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [Corruptite([-1, -1], 5)], 1, [[Gold([-1, -1], 12), 0.7], [SteelPickaxe([-1, -1]), 0.1], [[Corruptite([-1, -1], 2)], 0.2]], 45, 3)

class RockwormJaws(Weapon):
    def __init__(self, ):
        super().__init__("Jaws", "33", [-1, -1], 0, 0, 0, "One-Handed Mace", 1, 1.25, [[lookup_damage_type_id("Piercing"), 10, 3], [lookup_damage_type_id("Blunt"), 10, 0]], [], None)

# Mine and Corruptite Mine
class RockWorm(Creature):
    def __init__(self, pos):
        super().__init__("Tunneler", "33", pos, [CreatureSegment(self, "33", (pos[0] + 1, pos[1]), "Fluid"), CreatureSegment(self, "33", (pos[0], pos[1] + 1), "Fluid"), CreatureSegment(self, "33", (pos[0] + 1, pos[1] + 1), "Fluid")], 50, 0, 1, [], 5, 2, 0, 0, 0.2, 999,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [RockwormJaws, None, None, None, None, None, None, None, None], [], [0.5, 0.9, 0.0, 0.7, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.3, 0.0, 0.0],
                         [0.7, 0.9, 0.7, 1.0, 0.0, 1.0, 0.2, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0], [], 0, [], 50, 5)
    def basic_attack(self, grid, target):
        if isinstance(target, Wall):
            grid[target.pos[0]][target.pos[1]].remove(target)
            return
        if self.basic_attack_hit_check(grid, 5, False, target):
            self.basic_attack_damage(grid, RockwormJaws(), target, self.crit_check(grid))

# Mine and Corruptite Mine
class Troll(Creature):
    def __init__(self, pos):
        super().__init__("Troll", "22", pos, [CreatureSegment(self, "22", (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, "22", (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, "22", (pos[0] + 1, pos[1] + 1), "Static")], 75, 0, 1, [Regeneration(5, True)], 12, 0, 0, 0, 0.05, 10,
                         [0, 0, 7, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (WoodenGreatclub((-1, -1), None), None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, [], 80, 5)

class CorruptJaws(Weapon):
    def __init__(self, ):
        super().__init__("Jaws", "33", [-1, -1], 0, 0, 0, "One-Handed Mace", 1, 2, [[lookup_damage_type_id("Piercing"), 10, 3], [lookup_damage_type_id("Blunt"), 10, 0], [lookup_damage_type_id("Dark"), 5, 3]], [Bleed(5, False)], None)


#Corruptite Mine
class CorruptWorm(Creature):
    def __init__(self, pos):
        super().__init__("Corrupted Tunneler", "22", pos, [CreatureSegment(self, "33", (pos[0] + 1, pos[1]), "Fluid"), CreatureSegment(self, "33", (pos[0], pos[1] + 1), "Fluid"), CreatureSegment(self, "33", (pos[0] + 1, pos[1] + 1), "Fluid")], 100, 0, 1, [], 7, 2, 0, 0, 0.3, 999,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [CorruptJaws, None, None, None, None, None, None, None, None], [], [0.5, 0.9, 0.0, 0.7, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.3, 1.0, 0.0],
                         [0.7, 0.9, 0.7, 1.0, 0.0, 1.0, 0.2, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0], [], 0, [[[Corruptite([-1, -1], 2)], 1.0]], 70, 7)
    def basic_attack(self, grid, target):
        if isinstance(target, Wall):
            grid[target.pos[0]][target.pos[1]].remove(target)
            return
        if self.basic_attack_hit_check(grid, 5, False, target):
            self.basic_attack_damage(grid, CorruptJaws(), target, self.crit_check(grid))

# Mine and Corruptite Mine
class CorruptTroll(Creature):
    def __init__(self, pos):
        super().__init__("Corrupt Troll", "22", pos, [CreatureSegment(self, "22", (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, "22", (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, "22", (pos[0] + 1, pos[1] + 1), "Static")], 125, 0, 1, [Regeneration(10, True)], 15, 0, 0, 0, 0.1, 10,
                         [0, 0, 7, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (WoodenGreatclub((-1, -1), None), None, None, None, None, None, None, None, None), [BloodBurst()], [0.7, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0],
                         basicStatusResistances, [], 0, [[[Corruptite([-1, -1], 2)], 1.0]], 90, 7)

class BehemothSlam(Weapon):
    def __init__(self, ):
        super().__init__("Slam", "33", [-1, -1], 0, 0, 0, "One-Handed Mace", 1, 2, [[lookup_damage_type_id("Piercing"), 5, 3], [lookup_damage_type_id("Blunt"), 20, 0], [lookup_damage_type_id("Dark"), 10, 5]], [Bleed(7, False)], None)


# boss in Corruptite Mine 2
class CorruptBehemoth(Boss):
    def __init__(self, pos):
        super().__init__("Corrupted Behemoth", "22", pos, [CreatureSegment(self, "22", [pos[0] + 1, pos[1]],  "Static"), CreatureSegment(self, "22", [pos[0] + 2, pos[1]],  "Static"), CreatureSegment(self, "22", [pos[0], pos[1] + 1], "Static"), CreatureSegment(self, "22", [pos[0] + 1, pos[1] + 1], "Static"), CreatureSegment(self, "22", [pos[0] + 2, pos[1] + 1],  "Static"), CreatureSegment(self, "22", [pos[0], pos[1] + 2], "Static"), CreatureSegment(self, "22", [pos[0] + 1, pos[1] + 2], "Static"), CreatureSegment(self, "22", [pos[0] + 2, pos[1] + 2],  "Static")], 250, 0, 1, [], 20, 0, 0, 0, 0.2,
                         (BehemothSlam(), None, None, None, None, None, None, None, None),
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), [ShardShot()],
                         [0.5, 0.9, 0.0, 0.7, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.3, 1.0, 0.0], [0.7, 0.9, 0.7, 0.0, 0.0, 1.0, 0.2, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0], [], 0, [[[Corruptite([-1, -1], 5)], 1.0]], 200, 10)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 10, False, target):
            self.basic_attack_damage(grid, BehemothSlam(), target, self.crit_check(grid))

class Dissolve(Weapon):
    def __init__(self, ):
        super().__init__("Slam", "33", [-1, -1], 0, 0, 0, "One-Handed Mace", 1, 1.25, [[lookup_damage_type_id("Acid"), 7, 3]], [], None)

# sewer
class GiantSlime(Creature):
    def __init__(self, pos):
        super().__init__("Giant Slime", "22", pos, [CreatureSegment(self, "22", (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, "22", (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, "22", (pos[0] + 1, pos[1] + 1), "Static")], 40, 0, 1, [], 4, 0, 0, 2, 0.1, 10,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (Dissolve(), None, None, None, None, None, None, None, None), [], [1.0, 0.7, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0],
                         [1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0], [], 0, [], 30, 3)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 5, False, target):
            self.basic_attack_damage(grid, Dissolve(), target, self.crit_check(grid))
    def die(self, grid, player, corpse):
        grid[self.pos[0]][self.pos[1]].append(Slime(self.pos))
        grid[self.pos[0] + 1][self.pos[1]].append(Slime([self.pos[0] + 1, self.pos[1]]))
        grid[self.pos[0]][self.pos[1] + 1].append(Slime([self.pos[0], self.pos[1] + 1]))
        grid[self.pos[0] + 1][self.pos[1] + 1].append(Slime([self.pos[0] + 1, self.pos[1] + 1]))
        super().die(grid, player, corpse)


class Slime(Creature):
    def __init__(self, pos):
        super().__init__("Slime", "22", pos, [], 10, 0, 1, [], 2, 0, 0, 3, 0.1, 10,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (Dissolve(), None, None, None, None, None, None, None, None), [], [1.0, 0.7, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0],
                         [1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0], [], 0, [], 10, 1)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 3, False, target):
            self.basic_attack_damage(grid, Dissolve(), target, self.crit_check(grid))

# sewer
class Frogman(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = SteelSpear((-1, -1), None)
        else:
            weapon = Sling((-1, -1), None)
        super().__init__("Frogman", "22", pos, [], 20, 0, 1, [], 3, 3, 0, 3, 0.3, 10,
                         (7, 7, 7, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 5, 5, 5, 5),
                         (weapon, None, None, None, None, None, None, None, None), [], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.25, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 1.0, 0.25, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [Pebble([-1, -1], 16)], 1, [[Gold((-1, -1), 7), 0.7]], 20, 2)

# sewer
#giant lobster-type creature that eats trash
class TrashLobster(Creature):
    def __init__(self, pos):
        super().__init__("Refuse Ravager", "22", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 50, 0, 1, [], 5, 3, 0, 2, 0.2, 10,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (CrusherClaw(), PincerClaw(), None, None, None, None, None, None, None), [FetidBreath()], (0.6, 0.6, 0.6, 0.0, 0.0, 1.0, 0.5, 0.0, 1.0, 0.0, 0.3, 0.0, 0.0),
                         (0.8, 0.4, 0.0, 0.7, 0.3, 0.0, 1.0, 0.0, 0.0, 0.4, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0), [], 0, [], 80, 5)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 3, False, target):
            self.basic_attack_damage(grid, CrusherClaw(), target, self.crit_check(grid))
        if self.basic_attack_hit_check(grid, 5, False, target):
            self.basic_attack_damage(grid, PincerClaw(), target, self.crit_check(grid))

class CrocJaws(Weapon):
    def __init__(self, ):
        super().__init__("Jaws", "33", [-1, -1], 0, 0, 0, "One-Handed Mace", 1, 1.5, [[lookup_damage_type_id("Piercing"), 10, 3], [lookup_damage_type_id("Blunt"), 10, 0]], [Bleed(5, False)], None)

# sewer
class SewerCroc(Creature):
    def __init__(self, pos):
        super().__init__("Sewer Crocodile", "22", pos, [], 40, 0, 1, [], 5, 5, 0, 3, 0.5, 15,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (CrocJaws(), None, None, None, None, None, None, None, None), [], [0.1, 0.3, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                         [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [], 0, [], 30, 3)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 20, False, target):
            self.basic_attack_damage(grid, CrocJaws(), target, self.crit_check(grid))

class FishJaws(Weapon):
    def __init__(self, ):
        super().__init__("Jaws", "33", [-1, -1], 0, 0, 0, "One-Handed Blade", 1, 2, [[lookup_damage_type_id("Piercing"), 30, 10]], [Bleed(10, False)], None)

# sewer
class Gorefish(Creature):
    def __init__(self, pos):
        super().__init__("Gorefish", "22", pos, [], 40, 0, 1, [], 5, 5, 0, 5, 0.25, 15,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (FishJaws(), None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [], 0, [], 40, 4)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 7, False, target):
            self.basic_attack_damage(grid, FishJaws(), target, self.crit_check(grid))

# sewer
class Psyfish(Creature):
    def __init__(self, pos):
        super().__init__("Psyfish", "22", pos, [], 30, 100, 1, [], 1, 2, 7, 3, 0.1, 30,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0),
                         (None, None, None, None, None, None, None, None, None), [Confuse(), Overwhelm()], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.75, 0.5],
                         [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.75, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0], [], 0, [], 50, 5)
    def basic_attack(self, grid, target):
        return False

# sewer
class MasterThief(Creature):
    def __init__(self, pos):
        super().__init__("Master Thief", "22", pos, [], 20, 0, 1, [], 2, 10, 0, 10, 0.75, 20,
                         (15, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 5, 0, 7, 10),
                         (SteelDagger([-1, -1], Enchantment("Poison", 5, 600, [], [Poison(6, False)])), SteelDagger([-1, -1], Enchantment("Poison", 5, 600, [], [Poison(6, False)])), None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, [[Gold([-1, -1], 75), 0.5], [MediumPoison([-1, -1], 1), 0.75]], 50, 5)


# Shantytown
class DiseasedScavenger(Creature):
    def __init__(self, pos):
        weapon_choice_one = random.randint(0, 5)
        if weapon_choice_one == 0:
            weapon_one = IronDagger((-1, -1), None)
        elif weapon_choice_one == 1:
            weapon_one = IronShortsword((-1, -1), None)
        elif weapon_choice_one == 2:
            weapon_one = IronHatchet((-1, -1), None)
        elif weapon_choice_one == 3:
            weapon_one = WoodenClub((-1, -1), None)
        elif weapon_choice_one == 4:
            weapon_one = IronSpear((-1, -1), None)
        else:
            weapon_one = Sling((-1, -1), None)
        weapon_choice_two = random.randint(0, 6)
        if weapon_choice_two == 0:
            weapon_two = IronDagger((-1, -1), None)
        elif weapon_choice_two == 1:
            weapon_two = IronShortsword((-1, -1), None)
        elif weapon_choice_two == 2:
            weapon_two = IronHatchet((-1, -1), None)
        elif weapon_choice_two == 3:
            weapon_two = WoodenClub((-1, -1), None)
        elif weapon_choice_two == 4:
            weapon_two = IronSpear((-1, -1), None)
        elif weapon_choice_two == 5:
            weapon_two = Sling((-1, -1), None)
        else:
            weapon_two = WoodenBuckler((-1, -1), None)
        super().__init__("Diseased Scavenger", "22", pos, [], 20, 0, 1, [], 3, 7, 0, 7, 0.25, 30,
                         (7, 7, 7, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 10, 0, 10, 0, 10, 10, 10, 10),
                         (weapon_one, weapon_two, None, None, None, None, None, None, None), [], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [Pebble([-1, -1], 16)], 1, [[Gold([-1, -1], 30), 0.5], [Antidote([-1, -1], 1), 0.75]], 20, 2)

# Shantytown
class BloatedGuard(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = SteelShortsword((-1, -1), None)
        else:
            weapon = SteelSpear((-1, -1), None)
        super().__init__("Bloated Guard", "22", pos, [], 75, 0, 1, [], 7, 2, 0, 1, 0.2, 10,
                         (10, 10, 10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),
                         (weapon, SteelShield([-1, -1], False), SteelHelmet([-1, -1], False), None, None, SteelBoots([-1, -1], False), None, None, None), [Retch()], [0.175, 0.2625, 0.2, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [], 0, [[Gold([-1, -1], 20), 0.75], [weapon, 0.75]], 40, 5)

class FlyJaws(Weapon):
    def __init__(self, enchantment):
        super().__init__("Jaws", "33", [-1, -1], 0, 0, 0, "One-Handed Blade", 1, 2, [[lookup_damage_type_id("Piercing"), 5, 2]], [Poison(15, False)], enchantment)

# Shantytown
class Stinkfly(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        super().__init__("Stinkfly", "22", pos, [], 15, 0, 1, [Flight(1, True)], 3, 8, 0, 8, 0.25, 15,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (FlyJaws(None), None, None, None, None, None, None, None, None), [Retch(), Buzz()], [0.0, 0.25, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [], 0, [], 30, 3)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 5, False, target):
            self.basic_attack_damage(grid, FlyJaws(None), target, self.crit_check(grid))

class Maggot(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        super().__init__("Maggot", "22", pos, [], 10, 0, 1, [], 3, 0, 0, 1, 0.25, 5,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (FlyJaws(None), None, None, None, None, None, None, None, None), [], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [], 0, [], 0, 0)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 4, False, target):
            self.basic_attack_damage(grid, FlyJaws(None), target, self.crit_check(grid))

#target must be tile where it is valid to place a new creature
class BirthMaggot(ActiveAbility):
    def __init__(self):
        super().__init__("Birth", "1", 0, 5, 0, 1, "")
    def use(self, grid, caster, target):
        super().use(grid, caster, target)
        grid[target.pos[0]][target.pos[1]].append(Maggot(target.pos))

# Shantytown 2 boss
class Rotmother(Boss):
    def __init__(self, pos):
        super().__init__("Rotmother", "22", pos, [CreatureSegment(self, "22", [pos[0] + 1, pos[1]],  "Static"), CreatureSegment(self, "22", [pos[0] + 2, pos[1]],  "Static"), CreatureSegment(self, "22", [pos[0], pos[1] + 1], "Static"), CreatureSegment(self, "22", [pos[0] + 1, pos[1] + 1], "Static"), CreatureSegment(self, "22", [pos[0] + 2, pos[1] + 1],  "Static"), CreatureSegment(self, "22", [pos[0], pos[1] + 2], "Static"), CreatureSegment(self, "22", [pos[0] + 1, pos[1] + 2], "Static"), CreatureSegment(self, "22", [pos[0] + 2, pos[1] + 2],  "Static")], 300, 0, 1, [], 10, 0, 0, 0, 0.75,
                         (FlyJaws(Decay()), None, None, None, None, None, None, None, None),
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), [BirthMaggot(), Retch()],
                         [0.0, 0.25, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [], 0, [], 200, 10)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 10, False, target):
            self.basic_attack_damage(grid, FlyJaws(Decay()), target, self.crit_check(grid))

class MagmaGolemSlam(Weapon):
    def __init__(self, ):
        super().__init__("Slam", "33", [-1, -1], 0, 0, 0, "One-Handed Mace", 1, 1.25, [[lookup_damage_type_id("Blunt"), 15, 0], [lookup_damage_type_id("Fire"), 10, 5]], [Burning(10, False)], None)

# magma Core
class MagmaGolem(Creature):
    def __init__(self, pos):
        super().__init__("Magma Golem", "22", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 150, 0, 1, [], 5, 0, 0, 1, 0.1, 10,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (MagmaGolemSlam(), None, None, None, None, None, None, None, None), [], [0.6, 0.8, 0.9, 1.0, 0.9, 0.0, -1.0, 0.5, 1.0, 1.0, 1.0, 0.0, 0.0],
                         [1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0], [], 0, [], 50, 5)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 10, False, target):
            self.basic_attack_damage(grid, MagmaGolemSlam(), target, self.crit_check(grid))

class SpriteBurn(Weapon):
    def __init__(self, ):
        super().__init__("Burn", "33", [-1, -1], 0, 0, 0, "One-Handed Blade", 1, 1.25, [[lookup_damage_type_id("Fire"), 5, 3]], [Burning(1, False)], None)

# magma core and embers
class FireSprite(Creature):
    def __init__(self, pos):
        super().__init__("Fire Sprite", "22", pos, [], 5, 0, 1, [Flight(1, True)], 0, 3, 0, 3, 0.1, 10,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (SpriteBurn(), None, None, None, None, None, None, None, None), [], [1.0, 1.0, 1.0, 1.0, 0.9, -1.0, -2.0, 0.5, 1.0, 0.0, 1.0, 0.0, 0.0],
                         [1.0, 1.0, 1.0, 0.0, -1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0], [], 0, [], 30, 3)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 3, False, target):
            self.basic_attack_damage(grid, SpriteBurn(), target, self.crit_check(grid))

class ElementalBurn(Weapon):
    def __init__(self, ):
        super().__init__("Burn", "33", [-1, -1], 0, 0, 0, "One-Handed Blade", 1, 1.5, [[lookup_damage_type_id("Fire"), 10, 3]], [Burning(5, False)], None)

# magma core
class FireElemental(Creature):
    def __init__(self, pos):
        super().__init__("Fire Elemental", "22", pos, [], 15, 50, 1, [], 3, 3, 0, 3, 0.1, 10,
                         (5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),
                         (ElementalBurn(), None, None, None, None, None, None, None, None), [FireBolt(), Fireball()], [1.0, 1.0, 1.0, 1.0, 0.9, -1.0, -2.0, 0.5, 1.0, 0.0, 1.0, 0.0, 0.0],
                         [1.0, 1.0, 1.0, 0.0, -1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0], [], 0, [], 30, 3)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 10, False, target):
            self.basic_attack_damage(grid, ElementalBurn(), target, self.crit_check(grid))

# Deep Cave and undercity
class DarkElf(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon_one = MithrilShortsword((-1, -1), Darkness())
            weapon_two = MithrilShortsword((-1, -1), Darkness())
        else:
            weapon_one = SilverwoodLongbow((-1, -1), Darkness())
            weapon_two = Unavailable()
        super().__init__("Dark Elf", "22", pos, [], 50, 0, 2, [], 3, 7, 0, 7, 0.5, 999,
                         (10, 10, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 10, 0, 10, 0, 10, 10, 10, 10),
                         (weapon_one, weapon_two, None, LeatherCuirass([-1, -1], None), None, LeatherBoots([-1, -1], None), None, None, None), [], [0.15, 0.2, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.7, 0.5],
                         basicStatusResistances, [Arrow([-1, -1], 16)], 1, [[Gold([-1, -1], 20), 1.0], [Arrow([-1, -1], 5), 0.75]], 80, 8)

# Deep Cave
class DarkDwarf(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon_one = AdamantineAxe((-1, -1), None)
            weapon_two = AdamantineShield((-1, -1), None)
            piercing_resist = 0.8
            slashing_resist = 0.95
        else:
            weapon_one = AdamantineGreataxe((-1, -1), None)
            weapon_two = Unavailable()
            piercing_resist = 0.625
            slashing_resist = 0.75
        super().__init__("Dark Dwarf", "22", pos, [], 60, 0, 1, [], 6, 1, 0, 1, 0.2, 999,
                         (15, 15, 15, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),
                         (weapon_one, weapon_two, AdamantineHelmet((-1, -1), None), AdamantineBreastplate((-1, -1), None), AdamantineGreaves((-1, -1), None), AdamantineBoots((-1, -1), None), None, None, None), [], [piercing_resist, slashing_resist, 0.0, 0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0],
                         [0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0], [], 0, [[Gold((-1, -1), 90), 0.6]], 90, 9)

class UlnSlam(Weapon):
    def __init__(self, ):
        super().__init__("Slam", "33", [-1, -1], 0, 0, 0, "One-Handed Mace", 1, 1.25, [[lookup_damage_type_id("Blunt"), 15, 0]], [],None)

# Deep Cave
#giant blind salamander, mild magic abilities
class Uln(Creature):
    def __init__(self, pos):
        super().__init__("Uln", "22", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 100, 50, 1, [], 5, 0, 5, 2, 0.1, 999,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0),
                         (UlnSlam(), None, None, None, None, None, None, None, None), [], [0.0, 0.0, 0.5, 0.0, 0.0, 1.0, 0.7, 0.0, 1.0, 1.0, 0.0, 0.8, 0.5],
                         [0.0, 0.0, 0.0, 1.0, 0.5, 1.0, 0.0, 0.5, 0.3, 0.3, 0.0, 0.0, 0.0, -1.0, 0.0, 0.5, 0.0], [FireBolt(), LightningBolt(), IceBolt(), AcidBolt(), ArcaneBolt()], 0, [], 90, 9)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 7, False, target):
            self.basic_attack_damage(grid, UlnSlam(), target, self.crit_check(grid))

# Deep Cave
#giant blind salamander, strong magic abilities
class ElderUln(Creature):
    def __init__(self, pos):
        super().__init__("Elder Uln", "22", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 100, 200, 1, [], 5, 0, 12, 2, 0.1, 999,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 15, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0),
                         (UlnSlam(), None, None, None, None, None, None, None, None), [], [0.0, 0.0, 0.5, 0.0, 0.0, 1.0, 0.7, 0.0, 1.0, 1.0, 0.0, 0.9, 0.6],
                         [0.0, 0.0, 0.0, 1.0, 0.5, 1.0, 0.0, 0.5, 0.3, 0.3, 0.0, 0.0, 0.0, -1.0, 0.0, 0.5, 0.0], [Fireball(), TidalWave(), Freeze(), PoisonCloud()], 0, [], 90, 9)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 7, False, target):
            self.basic_attack_damage(grid, UlnSlam(), target, self.crit_check(grid))

class ToadTounge(Weapon):
    def __init__(self, ):
        super().__init__("Slam", "33", [-1, -1], 0, 0, 0, "One-Handed Mace", 5, 1.25, [[lookup_damage_type_id("Blunt"), 10, 0]], [],None)

# Deep Cave
class CaveToad(Creature):
    def __init__(self, pos):
        super().__init__("Cave Toad", "22", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 80, 0, 1, [], 8, 1, 0, 1, 0.1, 999,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (ToadTounge(), None, None, None, None, None, None, None, None), [], [0.3, 0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 0.3, 1.0, 1.0, 0.0, 0.0, 0.0],
                         [0.3, 0.5, 0.0, 1.0, 0.0, 1.0, 0.5, 0.5, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0], [], 0, [], 50, 5)

class GiantSpiderFangs(Weapon):
    def __init__(self):
        super().__init__("Fang", "17", (-1, -1), 0, 0, 0, "One-Handed Blade", 1, 1.5,
                         [(lookup_damage_type_id("Piercing"), 15, 1)], [Poison(7, False)], None)

# Deep Cave
class GiantSpider(Creature):
    def __init__(self, pos):
        super().__init__("Giant Spider", "22", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 60, 0, 1, [], 4, 3, 0, 0.3, 0.5, 999,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (GiantSpiderFangs(), None, None, None, None, None, None, None, None), [], [0.5, 0.7, 0.3, 0.0, 0.0, 1.0, 0.0, 0.4, 1.0, 1.0, 0.2, 0.0, 0.0],
                         [0.7, 0.5, 0.0, 0.0, 0.0, 1.0, 0.1, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0], [], 0, [], 80, 8)

# Deep Cave
class CaveGiant(Creature):
    def __init__(self, pos):
        super().__init__("Cave Giant", "22", pos, [CreatureSegment(self, "22", [pos[0] + 1, pos[1]],  "Static"), CreatureSegment(self, "22", [pos[0] + 2, pos[1]],  "Static"), CreatureSegment(self, "22", [pos[0], pos[1] + 1], "Static"), CreatureSegment(self, "22", [pos[0] + 1, pos[1] + 1], "Static"), CreatureSegment(self, "22", [pos[0] + 2, pos[1] + 1],  "Static"), CreatureSegment(self, "22", [pos[0], pos[1] + 2], "Static"), CreatureSegment(self, "22", [pos[0] + 1, pos[1] + 2], "Static"), CreatureSegment(self, "22", [pos[0] + 2, pos[1] + 2],  "Static")], 200, 0, 1, [], 30, 3, 0, 0, 0.1, 999,
                         (0, 0, 15, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (WoodenGreatclub([-1, -1]), None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, [[Gold([-1, -1], 20), 0.2], [WoodenGreatclub([-1, -1], None), 0.5],], 100, 10)

class Macuahuitl(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Macuahuitl", "17", pos, 6, 50, 5, "One-Handed Blade", 1, 2.5,
                         [[lookup_damage_type_id("Slashing"), 15, 8]], [Bleed(7, False)], enchantment)

class LargeMacuahuitl(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Large Macuahuitl", "17", pos, 6, 50, 20, "Two-Handed Blade", 1, 3,
                         [[lookup_damage_type_id("Slashing"), 30, 10]], [Bleed(10, False)], enchantment)

class HideShield(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Hide Shield", "42", pos, 3, 30, 3, "Hands", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.03
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.05

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.03
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.05

# Ziggurat
class XotilWarrior(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon_one = Macuahuitl([-1, -1], Shadow())
            weapon_two = HideShield([-1, -1], None)
            pierce_resist = 0.03
            slash_resist = 0.05
        else:
            weapon_one = LargeMacuahuitl([-1, -1], Darkness())
            weapon_two = Unavailable()
            pierce_resist = 0.0
            slash_resist = 0.0
        super().__init__("Xotil Warrior", "22", pos, [], 50, 0, 1, [], 5, 5, 0, 5, 0.5, 15,
                         (0, 10, 0, 0, 10, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),
                         (weapon_one, weapon_two, None, None, None, None, None, None, None), [], [pierce_resist, slash_resist, 0.0, 0.1, 0.3, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                         [1.0, 0.5, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0], [], 0, [[Whetstone([-1, -1], 1), 0.7], [Macuahuitl([-1, -1], None), 0.05]], 80, 8)

class AbominationSlam(Weapon):
    def __init__(self, ):
        super().__init__("Slam", "33", [-1, -1], 0, 0, 0, "One-Handed Mace", 1, 1.25, [[lookup_damage_type_id("Blunt"), 20, 0]], [Bleed(5, False)],None)


# Ziggurat
class XotilAbomination(Creature):
    def __init__(self, pos):
        super().__init__("Xotil Abomination", "22", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 200, 0, 1, [Regeneration(10, True)], 20, 3, 0, 2, 0.1, 10,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (AbominationSlam(), None, None, None, None, None, None, None, None), [], [0.5, 0.8, 0.9, 0.3, 0.6, 1.0, 0.0, 0.3, 1.0, 1.0, 0.5, 0.5, 0.0],
                         [0.5, 0.5, 0.1, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.8, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0], [], 0, [], 100, 10)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 10, False, target):
            self.basic_attack_damage(grid, AbominationSlam(), target, self.crit_check(grid))

 #Ziggurat
class XotilPriest(Creature):
    def __init__(self, pos):
        super().__init__("Xotil Priest", "22", pos, [], 50, 200, 1, [], 1, 2, 15, 2, 0.1, 15,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 15, 15, 15, 15, 0, 0, 0, 0, 0, 0, 2, 0),
                         (WoodenClub([-1, -1], None), None, None, None, None, None, None, None, None), [Exsanguinate(), SiphonBlood()], [0.0, 0.0, 0.0, 0.1, 0.3, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                         [1.0, 0.5, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0], [], 0, [[FlayScroll([-1, -1], 1), 0.2]], 100, 10)

class SerpentFangs(Weapon):
    def __init__(self, ):
        super().__init__("Fangs", "33", [-1, -1], 0, 0, 0, "One-Handed Blade", 1, 2, [[lookup_damage_type_id("Piercing"), 15, 0]], [Bleed(10, False)],None)

#Ziggurat
#A ferocious serpent made out of obsidian and blood
class DarkSerpent(Creature):
    def __init__(self, pos):
        super().__init__("Dark Serpent", "22", pos, [CreatureSegment(self, "33", (pos[0] + 1, pos[1]), "Fluid"), CreatureSegment(self, "33", (pos[0], pos[1] + 1), "Fluid"), CreatureSegment(self, "33", (pos[0] + 1, pos[1] + 1), "Fluid"), CreatureSegment(self, "33", (pos[0], pos[1] + 2), "Fluid"), CreatureSegment(self, "33", (pos[0] + 1, pos[1] + 2), "Fluid")], 30, 0, 1, [], 5, 5, 0, 5, 0.5, 10,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (SerpentFangs(), None, None, None, None, None, None, None, None), [], [0.9, 1.0, 0.7, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 0.0, 0.0],
                         [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0], [], 0, [], 100, 10)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 15, False, target):
            self.basic_attack_damage(grid, SerpentFangs(), target, self.crit_check(grid))

class DarkRay(Weapon):
    def __init__(self, ):
        super().__init__("Ray", "33", [-1, -1], 0, 0, 0, "One-Handed Blade", 5, 2, [[lookup_damage_type_id("Dark"), 20, 0]], [],None)

class DarkSun(Creature):
    def __init__(self, pos):
        super().__init__("Dark Sun", "22", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 30, 0, 1, [], 0, 0, 0, 0, 0.25, 20,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (DarkRay(), None, None, None, None, None, None, None, None), [], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                         [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [], 0, [], 0, 0)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 20, False, target):
            self.basic_attack_damage(grid, SerpentFangs(), target, self.crit_check(grid))

class SummonDarkSun(Spell):
    def __init__(self):
        super().__init__("Dark Sun", "45", 20, 100, 5, "Summoning")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        new_sun = DarkSun(target.pos)
        grid[target.pos[0]][target.pos[1]].append(new_sun)
        caster.suns.append(new_sun)

# Boss of Ziggurat 3
class XotilHighPriest(Boss):
    def __init__(self, pos):
        super().__init__("Xotil High Priest", "22", pos, [], 200, 500, 1, [], 1, 2, 30, 2, 0.1,
                         (WoodenClub([-1, -1], None), None, None, None, None, None, None, None, None), (0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 20, 20, 20, 20, 0, 0, 0, 0, 0, 0, 2, 0), [SummonDarkSun(), Exsanguinate(), SiphonBlood()], [0.0, 0.0, 0.0, 0.1, 0.3, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                         [1.0, 0.5, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0], [], 0, [FlayScroll([-1, -1], 1)], 200, 20)
        self.suns = []
    def die(self, grid, player, corpse):
        for sun in self.suns:
            sun.die(grid, player, corpse)
        super().die(grid, player, corpse)


# Undercity
class DarkElfSorceress(Creature):
    def __init__(self, pos):
        super().__init__("Dark Elf Sorceress", "22", pos, [], 70, 200, 1, [], 1, 5, 15, 5, 0.3, 999,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 15, 15, 15, 15, 0, 0, 0, 0, 0, 0, 2, 0),
                         (WoodenClub([-1, -1], None), None, None, None, None, None, None, None, None), [DarkShroud(), WickedRend()], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.7, 0.5],
                         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [], 0, [[Gold([-1, -1], 60), 0.7], [DarkShroudScroll([-1, -1], 1), 0.1]], 110, 11)

# Undercity
class Drider(Creature):
    def __init__(self, pos):
        super().__init__("Drider", "22", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 150, 0, 1, [], 10, 10, 10, 3, 0.3, 999,
                         [0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                         (MithrilHalberd([-1, -1], Darkness()), Unavailable(), None, None, None, None, None, None, None), [], [0.5, 0.7, 0.8, 0.0, 0.3, 1.0, 0.3, 0.0, 0.0, 1.0, 0.0, 0.7, 0.5],
                         [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Undercity
class DarkElfQueen(Boss):
    def __init__(self, pos):
        super().__init__("Dark Elf Queen", "22", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 300, 300, 1, [], 30, 5, 30, 3, 0.2,
                         (MithrilShortsword([-1, -1], Evil()), MithrilShortsword([-1, -1], Evil()), None, None, None, None, None, None, None),
                         [20, 0, 0, 0, 0, 0, 0, 0, 0, 20, 20, 20, 20, 20, 10, 0, 0, 0, 2, 0], [DarkShroud(), WickedRend(), Freeze()],
                         [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.7, 0.5], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [], 0, [MithrilShortsword([-1, -1], Evil()), WickedRendScroll([-1, -1], 1)], 200, 20)


class AshGolemSlam(Weapon):
    def __init__(self, ):
        super().__init__("Slam", "33", [-1, -1], 0, 0, 0, "One-Handed Mace", 1, 1.25, [[lookup_damage_type_id("Blunt"), 25, 0]], [Suffocation(20, False)], None)

# Embers and Columbarium
class AshGolem(Creature):
    def __init__(self, pos):
        super().__init__("Ash Golem", "22", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 170, 0, 1, [], 5, 0, 0, 1, 0.1, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (AshGolemSlam(), None, None, None, None, None, None, None, None), [], [0.6, 0.8, 1.0, 1.0, 0.9, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0, 0.0, 0.0],
                         [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0], [], 0, [], 60, 6)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 15, False, target):
            self.basic_attack_damage(grid, AshGolemSlam(), target, self.crit_check(grid))

class ObsidianGolemSlam(Weapon):
    def __init__(self, ):
        super().__init__("Slam", "33", [-1, -1], 0, 0, 0, "One-Handed Mace", 1, 1.25, [[lookup_damage_type_id("Blunt"), 15, 0], [lookup_damage_type_id("Piercing"), 15, 5]], [], None)

# Embers
class ObsidianGolem(Creature):
    def __init__(self, pos):
        super().__init__("Obsidian Golem", "22", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 150, 0, 1, [], 5, 0, 0, 1, 0.1, 10,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (ObsidianGolemSlam(), None, None, None, None, None, None, None, None), [], [1.0, 1.0, 0.0, 1.0, 0.9, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 0.0, 0.0],
                         [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0], [], 0, [], 60, 6)
    def basic_attack(self, grid, target):
        if self.basic_attack_hit_check(grid, 10, False, target):
            self.basic_attack_damage(grid, MagmaGolemSlam(), target, self.crit_check(grid))

class AshColossusSlam(Weapon):
    def __init__(self, ):
        super().__init__("Slam", "33", [-1, -1], 0, 0, 0, "One-Handed Mace", 1, 1.25, [[lookup_damage_type_id("Blunt"), 30, 0]], [Suffocation(40, False)], None)


# Boss of Embers
class AshColossus(Boss):
    def __init__(self, pos):
        super().__init__("Ash Colossus", "22", pos,
        [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0] + 2, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0] + 3, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0] + 4, pos[1]), "Static"),
                  CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 2, pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 3, pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 4, pos[1] + 1), "Static"),
                  CreatureSegment(self, 22, (pos[0], pos[1] + 2), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 2), "Static"), CreatureSegment(self, 22, (pos[0] + 2, pos[1] + 2), "Static"), CreatureSegment(self, 22, (pos[0] + 3, pos[1] + 2), "Static"), CreatureSegment(self, 22, (pos[0] + 4, pos[1] + 2), "Static"),
                  CreatureSegment(self, 22, (pos[0], pos[1] + 3), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 3), "Static"), CreatureSegment(self, 22, (pos[0] + 2, pos[1] + 3), "Static"), CreatureSegment(self, 22, (pos[0] + 3, pos[1] + 3), "Static"), CreatureSegment(self, 22, (pos[0] + 4, pos[1] + 3), "Static"),
                  CreatureSegment(self, 22, (pos[0], pos[1] + 4), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 4), "Static"), CreatureSegment(self, 22, (pos[0] + 2, pos[1] + 4), "Static"), CreatureSegment(self, 22, (pos[0] + 3, pos[1] + 4), "Static"), CreatureSegment(self, 22, (pos[0] + 4, pos[1] + 4), "Static"),],
                        300, 0, 1, [], 30, 0, 0, 0, 0.1,
                         (AshColossusSlam(), None, None, None, None, None, None, None, None),
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [],
                         [0.6, 0.8, 1.0, 1.0, 0.9, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0, 0.0, 0.0],
                         [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0], [], 0, [], 200, 20)


# Columbarium
class AshGhoul(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("AshGhoul", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Columbarium
class AshWight(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("AshWight", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

 #Columbarium and Catacomb and Necropolis
class Ghost(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("AshGhoul", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

#Columbarium and Catacomb and Necropolis
class Wraith(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Wraith", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)



# Catacomb and Necropolis
class Skeleton(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Skeleton", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Catacomb and Necropolis
class Zombie(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Zombie", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# Catacomb and Necropolis
class Ghoul(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Ghoul", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Catacomb and Necropolis
class Ghast(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Ghast", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Catacomb and Necropolis
class Wight(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Wight", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# Catacomb
class Necromancer(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Necromancer", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Catacomb
class Vampire(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Vampire", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# Carrion
class FleshAmalgam(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Flesh Amalgam", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Carrion
class Polyp(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Polyp", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Carrion
#seemingly human looking but without a soul or much higher intelligence
class Blank(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Blank", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Carrion
#an unfinished blank, no skin and bleeds everywhere
class Unfinished(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Unfinished", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# Worldeater’s Gut
class Parasite(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Parasite", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Worldeater’s Gut
class BloodCrawler(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Bloodcrawler", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Worldeater’s Gut
class Devourer(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Devourer", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Worldeater’s Gut 2
class WorldeaterHeart(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Worldeater's Heart", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None),
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [],
                         basicDamageResistances, basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Necropolis
class Lich(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Lich", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Necropolis
class DeathKnight(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Death Knight", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Necropolis
class WraithLord(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Wraith Lord", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Necropolis
class DeadKing(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("King of the Dead", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None),
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [],
                         basicDamageResistances, basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# Underworld
class Imp(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Imp", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld
class Demon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Demon", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld
class Hellhound(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Hellhound", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld
class Hellbat(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Hellbat", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld 1
class TricksterImp(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Trickster Imp", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld 1
class ConfusedSoul(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Confused Soul", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# Underworld 1
class DeceitDemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Demon of Deceit", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Underworld 1
class DeceitArchdemon(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Archdemon of Deceit", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None),
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [],
                         basicDamageResistances, basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld 2
class AngryImp(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Angry Imp", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld 2
class RageDemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Demon of Rage", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Underworld 2
class RageArchdemon(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Archdemon of Rage", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None),
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [],
                         basicDamageResistances, basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld 3
class CovetousImp(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Covetous Imp", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld 3
class CharitableSoul(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Charitable Soul", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld 3
class GreedDemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Demon of Greed", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Underworld 3
class GreedArchdemon(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Archdemon of Greed", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None),
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [],
                         basicDamageResistances, basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld 4
class SadImp(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Sad Imp", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld 4
class LostSoul(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Lost Soul", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld 4
class DepressedDemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Demon of Depression", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Underworld 4
class HopelessArchdemon(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Archdemon of Hopelessness", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None),
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [],
                         basicDamageResistances, basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld 5
class PeacefulSoul(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Peaceful Soul", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Underworld 5
class FateDemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Demon of Fate", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# Underworld 5
class FinalDemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Demon of Finality", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Underworld 5
class DoomArchdemon(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Archdemon of Doom", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None),
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [],
                         basicDamageResistances, basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Ancient City
#Strange constructs of stone and clockwork that servet the new gods
class AncientServant(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Ancient Servant", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Ancient City
class Apparition(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Apparition", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Ancient City
class Memory(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Memory of the Past", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

#The bosses of the Ancient City, the new gods, will be the same gods that you can choose to worship throughout the game so as I come up with gods to worship I will also add them here. The one you are currently worshipping cannot spawn as a boss.

# Temple of the old ones
class Cultist(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Cultist", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Temple of the old ones
class Shambler(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Shambler", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Temple of the old ones
class WrithingOne(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Writhing One", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Temple of the old ones
#Man builds up, he builds down
class DeepLord(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Lord of the Deep", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Temple of the old ones
#All descend from her
class Mother(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("The Mother", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Temple of the old ones
# He will be the only one left in the end
class Destroyer(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("The Destroyer", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Temple of the old ones
#He remembers all that has been forgotten
class Scholar(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("The Scholar", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Temple of the old ones
#You serve her whether you know it or not
class Schemer(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("The Schemer", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# Cosmic Void
class VoidBeast(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Void Beast", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Cosmic Void
class StarEater(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Star Eater", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Cosmic Void
class Annihilator(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Void Beast", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Cosmic Void
class GreatDreamer(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Great Dreamer", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None),
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Heart of the World , final boss
class AbyssDragon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Abyssal Dragon", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         (weapon, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)
