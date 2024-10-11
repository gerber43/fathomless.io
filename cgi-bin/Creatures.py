import random

from GameObject import Creature, CreatureSegment, Gold
from Items import IronDagger, WoodenClub

#Piercing, Slashing, Blunt, Fire, Lightning, Water, Cold, Acid, Light, Dark, Necrotic, Arcane, Existence
basicDamageResistances = (0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
#Bleed, Stun, Burning, Suffocation, Frozen, Blindness, Rot, Manadrain, Nonexistence, Poison, Fear, Confusion, Mindbreak, Bloodsiphon, Midas Curse, Death
basicStatusResistances = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

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
