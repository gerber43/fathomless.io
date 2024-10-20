import random

from GameObject import Creature, CreatureSegment, Gold
from Items import IronDagger, WoodenClub

#Piercing, Slashing, Blunt, Fire, Lightning, Water, Cold, Acid, Light, Dark, Necrotic, Arcane, Existence
basicDamageResistances = (0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
#Bleed, Stun, Burning, Suffocation, Frozen, Blindness, Rot, Manadrain, Nonexistence, Poison, Fear, Confusion, Mindbreak, Bloodsiphon, Midas Curse, Death
basicStatusResistances = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

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
class Goblin(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Goblin", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, (weapon, None, None, None, None, None, None, None, None, None), (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [], basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

#cave
class Bandit(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Bandit", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, (weapon, None, None, None, None, None, None, None, None, None), (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [], basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

#cave
class Ogre(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Ogre", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5, (weapon, None, None, None, None, None, None, None, None, None), (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [], basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

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
        super().__init__("Deep One", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# cove
class FishmanShaman(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Deep One Shaman", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# cove
class GiantCrab(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Bloodclaw", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
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

# cove
class Drowned(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Drowned", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# cove
class DrownedSailor(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Drowned Sailor", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# cove
class DrownedPirate(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Drowned Pirate", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))


# boss in cove 2
class DrownedCaptain(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Drowned Captain", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Mine and Corruptite Mine
class GoblinMiner(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Goblin Miner", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Mine and Corruptite Mine
class HobgoblinMiner(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Hobgoblin Miner", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Mine and Corruptite Mine
class RockWorm(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Tunneler", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Mine and Corruptite Mine
class Troll(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Troll", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Corruptite Mine
class CorruptWorm(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Corrupted Tunneler", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Corruptite Mine
class CorruptTroll(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Corrupted Troll", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))


# boss in Corruptite Mine 2
class CorruptBehemoth(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Corrupted Behemoth", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
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
        super().__init__("Giant Slime", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# sewer
class Frogman(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Frogman", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# sewer
#giant lobster-type creature that eats trash
class TrashLobster(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Refuse Ravager", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# sewer
class SewerCroc(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Sewer Crocodile", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# sewer
class Gorefish(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Gorefish", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# sewer
class Psyfish(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Psyfish", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# sewer
class MasterThief(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Master Thief", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))


# Shantytown
class DiseasedScavenger(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Diseased Scavenger", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Shantytown
class BloatedGuard(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Bloated Guard", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Shantytown
class Stinkfly(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Stinkfly", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Shantytown 2 boss
class Rotmother(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Rotmother", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
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
        super().__init__("Magma Golem", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# magma core and embers
class FireSprite(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Fire Sprite", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
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
        super().__init__("Fire Elemental", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
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
#giant blind salamander, mild magic abilities
class Uln(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Uln", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Deep Cave
#giant blind salamander, strong magic abilities
class ElderUln(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Elder Uln", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Deep Cave
class CaveToad(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Cave Toad", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Deep Cave
class CaveGiant(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Cave Giant", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
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
        super().__init__("Xotil Warrior", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
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
        super().__init__("Xotil Abomination", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

 #Ziggurat
class XotilPriest(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Xotil Priest", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

#Ziggurat
#A ferocious serpent made out of obsidian and blood
class DarkSerpent(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Dark Serpent", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Ziggurat 3
class XotilHighPriest(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Xotil High Priest", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Undercity
class DarkElfSorceress(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Dark Elf Sorceress", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Undercity
class Drider(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Drider", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Undercity
class DarkElfQueen(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Dark Elf Queen", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))


# Embers and Columbarium
class AshGolem(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Ash Golem", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Embers
class ObsidianGolem(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Obsidian Golem", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Embers
class AshColossus(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Obsidian Golem", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
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

 #Columbarium and Catacomb and Necropolis
class Ghost(Creature):
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

#Columbarium and Catacomb
class Wraith(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Wraith", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))



# Catacomb and Necropolis
class Skeleton(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Skeleton", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Catacomb and Necropolis
class Zombie(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Zombie", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))


# Catacomb and Necropolis
class Ghoul(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Ghoul", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Catacomb and Necropolis
class Ghast(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Ghast", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Catacomb and Necropolis
class Wight(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Wight", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))


# Catacomb
class Necromancer(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Necromancer", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Catacomb
class Vampire(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Vampire", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))


# Carrion
class FleshAmalgam(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Flesh Amalgam", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
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

# Carrion
#seemingly human looking but without a soul or much higher intelligence
class Blank(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Blank", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Carrion
#an unfinished blank, no skin and bleeds everywhere
class Unfinished(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Unfinished", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
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
class Bloodcrawler(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Bloodcrawler", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Worldeater’s Gut
class Devourer(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Devourer", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Worldeater’s Gut 2
class WorldeaterHeart(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Worldeater's Heart", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Necropolis
class Lich(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Lich", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
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
        super().__init__("Death Knight", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Necropolis
class WraithLord(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Wraith Lord", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))


# Underworld
class Imp(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Imp", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld
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

# Underworld
class Hellhound(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Hellhound", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld
class Hellbat(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Hellbat", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld 1
class TricksterImp(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Trickster Imp", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld 1
class ConfusedSoul(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Confused Soul", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))


# Underworld 1
class DeceitDemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Demon of Deceit", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Underworld 1
class DeceitArchdemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Archdemon of Deceit", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld 2
class AngryImp(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Angry Imp", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld 2
class RageDemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Demon of Rage", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Underworld 2
class RageArchdemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Archdemon of Rage", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld 3
class CovetousImp(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Covetous Imp", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld 3
class CharitableSoul(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Charitable Soul", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld 3
class GreedDemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Demon of Greed", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Underworld 3
class GreedArchdemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Archdemon of Greed", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld 4
class SadImp(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Sad Imp", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld 4
class LostSoul(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Lost Soul", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld 4
class DepressedDemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Demon of Depression", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Underworld 4
class HopelessArchdemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Archdemon of Hopelessness", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld 5
class PeacefulSoul(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Peaceful Soul", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Underworld 5
class FateDemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Demon of Fate", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))


# Underworld 5
class FinalDemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Demon of Finality", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Underworld 5
class DoomArchdemon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Archdemon of Doom", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Ancient City
#Strange constructs of stone and clockwork that servet the new gods
class AncientServant(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Ancient Servant", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Ancient City
class Apparition(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Apparition", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Ancient City
class Memory(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Memory of the Past", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

#The bosses of the Ancient City, the new gods, will be the same gods that you can choose to worship throughout the game so as I come up with gods to worship I will also add them here. The one you are currently worshipping cannot spawn as a boss.

# Temple of the old ones
class Cultist(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Cultist", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Temple of the old ones
class Shambler(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Shambler", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Temple of the old ones
class WrithingOne(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Writhing One", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Temple of the old ones
#Man builds up, he builds down
class DeepLord(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Lord of the Deep", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Temple of the old ones
#All descend from her
class Mother(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("The Mother", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Temple of the old ones
# He will be the only one left in the end
class Destroyer(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("The Destroyer", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Temple of the old ones
#He remembers all that has been forgotten
class Scholar(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("The Scholar", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Temple of the old ones
#You serve her whether you know it or not
class Schemer(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("The Schemer", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
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
        super().__init__("Void Beast", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Cosmic Void
class StarEater(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Star Eater", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Cosmic Void
class Annihilator(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Void Beast", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Boss of Cosmic Void
class GreatDreamer(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Great Dreamer", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))

# Heart of the World , final boss
class AbyssDragon(Creature):
    def __init__(self, pos):
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), 1)
        else:
            weapon = WoodenClub((-1, -1), 1)
        super().__init__("Abyssal Dragon", "22", pos, (), 10, 0, 1, [], 1, 5, 0, 0.3, 0.5,
                         (weapon, None, None, None, None, None, None, None, None, None),
                         (5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 2, 0, 5, 0), [],
                         basicDamageResistances, basicStatusResistances, (), 0, ((Gold((-1, -1), 3), 0.7)))
