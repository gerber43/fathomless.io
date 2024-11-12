#!/usr/bin/python3
import sys
import cgi
import random

from GameObject import Creature, CreatureSegment, Boss, Gold
from Items import *
from StatusEffects import Poison, Flight
from ActiveAbilities import *

#Piercing, Slashing, Blunt, Fire, Lightning, Water, Cold, Acid, Light, Dark, Necrotic, Arcane, Existence
basicDamageResistances = (0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
#Bleed, Stun, Burning, Suffocation, Frozen, Blindness, Rot, Manaburn, Nonexistence, Poison, Fear, Confusion, Mindbreak, Midas Curse, Bloodsiphon, Manadrain, Death
basicStatusResistances = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
#One-Handed Blades, One-Handed Axes, One-Handed Maces, Two-Handed Blades, Two-Handed Axes, Two-Handed Maces, Polearms, Slings, Bows, Elementalism, Cursing, Curse, Enhancement, Transmutation, Summoning, Dual-Wielding, Memory, Search, Hide, Lockpicking, Disarm Trap
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
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (weapon, shield, None, LeatherCuirass((-1, -1), None), None, None, None, None, None, None), [],
                         (0.025, 0.05, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 5), 0.7)), 20, 2)
        if shield is not None:
            self.damage_resistances[0] += 0.02
            self.damage_resistances[0] += 0.04

#cave
class Ogre(Creature):
    def __init__(self, pos):
        super().__init__("Ogre", "22", pos, [CreatureSegment(self, 22, (pos[0] + 1, pos[1]), "Static"), CreatureSegment(self, 22, (pos[0], pos[1] + 1), "Static"), CreatureSegment(self, 22, (pos[0] + 1, pos[1] + 1), "Static")], 50, 0, 1, [], 7, 0, 0, 0.0, 0.05, 10,
                         (0, 0, 5, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (WoodenGreatclub((-1, -1), None), None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, (), 50, 3)

class SpiderFangs(Weapon):
    def __init__(self):
        super().__init__("Fang", "17", (-1, -1), 0, 0, 0, "One-Handed Blade", 1, 1.5,
                         [(lookup_damage_type_id("Piercing"), 3, 1)], [Poison(3, False)], None)

# cave
class Spider(Creature):
    def __init__(self, pos):
        super().__init__("Spider", "26", pos, [], 10, 0, 1, [], 1, 3, 0, 4, 0.05, 20,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (SpiderFangs(), None, None, None, None, None, None, None, None, None), [], (0.3, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.6, 0.0, 0.0),
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
        super().__init__("Bat", "27", pos, [], 5, 0, 2, [Flight(1, True)], 1, 3, 0, 5, 0.05, 30,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (BatFangs(), None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0), [], 0, (), 5, 1)
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
                         (5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], (0.2, 0.5, 0.0, -0.5, -0.2, 2.0, 0.9, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0),
                         (0.9, 0.0, -0.5, 1.0, 0.9, 0.5, 0.0, 0.0, 0.0, 0.3, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0), [], 0, ((Gold((-1, -1), 7), 0.7)), 30, 3)

# cove
class FishmanShaman(Creature):
    def __init__(self, pos):
        super().__init__("Deep One Shaman", "22", pos, [IceBolt(), ChokingDeep()], 25, 50, 1, [], 0, 3, 5, 2, 0.05, 10,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0),
                         (CrusherClaw(), None, None, None, None, None, None, None, None, None), [], (0.2, 0.5, 0.0, -0.5, -0.2, 2.0, 0.9, 0.0, 1.0, 0.5, 0.0, 0.3, 0.0),
                         (0.9, 0.0, -0.5, 1.0, 0.9, 0.5, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), [LesserMana((-1, -1), 4)], 0, ((Gold((-1, -1), 7), 0.7), (LesserMana((-1, -1), 1), 0.2)), 40, 4)

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
                         (CrusherClaw(), PincerClaw(), None, None, None, None, None, None, None, None), [], (0.7, 0.7, 0.7, 0.0, 0.0, 1.0, 0.5, 0.0, 1.0, 0.0, 0.3, 0.0, 0.0),
                         (0.9, 0.5, 0.0, 0.7, 0.3, 0.0, 0.0, 0.0, 0.0, 0.4, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0), [], 0, (), 100, 6)
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
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Pirate", "29", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# cove
class Drowned(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Drowned", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# cove
class DrownedSailor(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Drowned Sailor", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# cove
class DrownedPirate(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Drowned Pirate", "30", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# boss in cove 2
class DrownedCaptain(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Drowned Captain", "31", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Mine and Corruptite Mine
class GoblinMiner(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Goblin Miner", "32", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Mine and Corruptite Mine
class HobgoblinMiner(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Hobgoblin Miner", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Mine and Corruptite Mine
class RockWorm(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Tunneler", "33", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Mine and Corruptite Mine
class Troll(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Troll", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Corruptite Mine
class CorruptWorm(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Corrupted Tunneler", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Corruptite Mine
class CorruptTroll(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Corrupted Troll", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# boss in Corruptite Mine 2
class CorruptBehemoth(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Corrupted Behemoth", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# sewer
class GiantSlime(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Giant Slime", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# sewer
class Frogman(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Frogman", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# sewer
#giant lobster-type creature that eats trash
class TrashLobster(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Refuse Ravager", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# sewer
class SewerCroc(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Sewer Crocodile", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# sewer
class Gorefish(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Gorefish", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# sewer
class Psyfish(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Psyfish", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# sewer
class MasterThief(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Master Thief", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# Shantytown
class DiseasedScavenger(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Diseased Scavenger", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Shantytown
class BloatedGuard(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Bloated Guard", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Shantytown
class Stinkfly(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Stinkfly", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Shantytown 2 boss
class Rotmother(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Rotmother", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# magma Core
class MagmaGolem(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Magma Golem", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# magma core and embers
class FireSprite(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Fire Sprite", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# magma core
class FireElemental(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Fire Elemental", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Deep Cave and undercity
class DarkElf(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("DarkElf", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Deep Cave
class DarkDwarf(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("DarkDwarf", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Deep Cave
#giant blind salamander, mild magic abilities
class Uln(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Uln", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Deep Cave
#giant blind salamander, strong magic abilities
class ElderUln(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Elder Uln", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Deep Cave
class CaveToad(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Cave Toad", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Deep Cave
class GiantSpider(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Giant Spider", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Deep Cave
class CaveGiant(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Cave Giant", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# Ziggurat
class XotilWarrior(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Xotil Warrior", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Ziggurat
class XotilAbomination(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Xotil Abomination", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

 #Ziggurat
class XotilPriest(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Xotil Priest", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

#Ziggurat
#A ferocious serpent made out of obsidian and blood
class DarkSerpent(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Dark Serpent", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Ziggurat 3
class XotilHighPriest(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Xotil High Priest", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Undercity
class DarkElfSorceress(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Dark Elf Sorceress", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Undercity
class Drider(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Drider", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Undercity
class DarkElfQueen(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Dark Elf Queen", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# Embers and Columbarium
class AshGolem(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Ash Golem", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Embers
class ObsidianGolem(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Obsidian Golem", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Embers
class AshColossus(Boss):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Obsidian Golem", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)


# Columbarium
class AshGhoul(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("AshGhoul", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)

# Boss of Cosmic Void
class GreatDreamer(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__("Great Dreamer", "22", pos, [], 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, 10,
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
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
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0),
                         (weapon, None, None, None, None, None, None, None, None, None), [], basicDamageResistances,
                         basicStatusResistances, [], 0, ((Gold((-1, -1), 3), 0.7)), 10, 1)
