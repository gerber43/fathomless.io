import random

from GameObject import Creature, CreatureSegment, Gold
from Items import IronDagger, WoodenClub

#Piercing, Slashing, Blunt, Fire, Lightning, Water, Cold, Acid, Light, Dark, Necrotic, Arcane, Existence
basicDamageResistances = (0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
#Bleed, Stun, Burning, Suffocation, Frozen, Blindness, Rot, Manadrain, Nonexistence, Poison, Fear, Confusion, Mindbreak, Bloodsiphon, Midas Curse, Death
basicStatusResistances = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

# cave
class Goblin(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Goblin", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, (weapon, None, None, None, None, None, None, None, None, None), (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [], basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))
        
class Player(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Player", "0", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, (weapon, None, None, None, None, None, None, None, None, None), (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [], basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))
class Boss(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Boss", "11", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, (weapon, None, None, None, None, None, None, None, None, None), (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [], basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# cave
class Spider(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Spider", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, (weapon, None, None, None, None, None, None, None, None, None), (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [], basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# cave
class Bat(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Bat", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# cove
class Fishman(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Fishman", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# cove
class UndeadSailor(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("UndeadSailor", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# cove
class Pirate(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Pirate", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))
# boss in cove 2
class Captain(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Captain", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Mine
class GoblinMiner(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("GoblinMiner", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Mine
class RockWorm(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("RockWorm", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))


# boss in Corruptite Mine 2
class CorruptedBehemoth(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("CorruptedBehemoth", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# sewer
class GiantSlime(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("GiantSlime", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# sewer
class SewerGator(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("SewerGator", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Shantytown
class DiseasedDenizen(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("DiseasedDenizen", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Shantytown
class BloatedScavenger(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("BloatedScavenger", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# magma Core
class MagmaGolem(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("MagmaGolem", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# magma core
class FireElemental(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("FireElemental", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Deep Cave and undercity
class DarkElf(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("DarkElf", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Deep Cave
class DarkDwarf(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("DarkDwarf", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Deep Cave
class DarkDwarf(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("DarkDwarf", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Ziggurat
class XotilWarrior(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("XotilWarrior", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Ziggurat
class XotilAbomination(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("XotilAbomination", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Ziggurat
class XotilHighPriest(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("XotilHighPriest", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Ember and Columbarium
class AshGolem(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("AshGolem", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Ember
class ObsidianGolem(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("ObsidianGolem", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Columbarium
class AshGhoul(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("AshGhoul", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Columbarium
class AshWight(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("AshWight", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Catacomb
class SkeletonSoldier(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("SkeletonSoldier", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Catacomb
class WraithLeader(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("WraithLeader", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Carrion
class FleshGolem(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("FleshGolem", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Carrion
class Polyp(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Polyp", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Worldeater’s Gut
class Parasite(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Parasite", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Worldeater’s Gut
class BloodCrawler(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("BloodCrawler", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Necropolis
class Liche(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Liche", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Necropolis
class DeathKnight(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("DeathKnight", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld
class Archdemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Archdemon", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# UnderWorld
class Demon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Demon", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Ancient City
class NewGodServant(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("NewGodServant", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Ancient City
class MistBeast(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("MistBeast", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Temple of the old one
class OldGodCultist(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("OldGodCultist", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Temple of the old one
class EldritchMinion(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("EldritchMinion", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Cosmic Void
class VoidBeast(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("VoidBeast", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Heart of the World , final boss
class CosmicDragon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("CosmicDragon", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))
