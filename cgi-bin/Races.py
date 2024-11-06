#!/usr/bin/python3
import sys
import cgi
from GameObject import Player
from ActiveAbilities import *

#Piercing, Slashing, Blunt, Fire, Lightning, Water, Cold, Acid, Light, Dark, Necrotic, Arcane, Existence
#Bleed, Stun, Burning, Suffocation, Frozen, Blindness, Rot, Manaburn, Nonexistence, Poison, Fear, Confusion, Mindbreak, Midas Curse, Bloodsiphon, Manadrain, Death

#TODO: Make humans get an extra skill point on levelup
class Human(Player):
    def __init__(self, name, pos):
        super().__init__(name, "38", pos, 3, 3, 0, 10, [], (0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
                         (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))

class Elf(Player):
    def __init__(self, name, pos):
        super().__init__(name, "38", pos, 1, 2, 3, 15, [], (0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.25, 0.25),
                         (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.1, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0))

class Dwarf(Player):
    def __init__(self, name, pos):
        super().__init__(name, "38", pos, 4, 2, 0, 10, [], (0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0),
                         (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0))

class Gnome(Player):
    def __init__(self, name, pos):
        super().__init__(name, "38", pos, 1, 2, 3, 10, [Blink()], (-0.5, -0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
                         (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
#class Orc(Player):

#class HalfDemon(Player):