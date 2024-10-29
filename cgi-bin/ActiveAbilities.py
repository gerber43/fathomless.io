#!/usr/bin/python3
import sys
import cgi
from SubSystem import ActiveAbility, Spell, Technique, Prayer

#player racial active abilities

#player-available spells
class HealingTouch(Spell):
    def __init__(self):
        super().__init__("Healing Touch", "1", 3, 20, "Enhancement")

    def use(self, grid, caster, target):
        pass

#player-available techniques

#prayers

#enemy-only active abilities

#enemy-only spells

#enemy-only techniques