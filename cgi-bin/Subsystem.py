#!/usr/bin/python3
import sys
import cgi
from abc import abstractmethod

#damage type and resistance subsystem, resistances are represented by a tuple of floats, use the following methods to figure out the indexes of specific  damage types and resistances
def lookup_damage_type_id(string):
    match string:
        case "Piercing":
            return 0
        case "PRC":
            return 0
        case "Slashing":
            return 1
        case "SLH":
            return 1
        case "Blunt":
            return 2
        case "BLT":
            return 2
        case "Fire":
            return 3
        case "FR":
            return 3
        case "Lightning":
            return 4
        case "LTG":
            return 4
        case "Water":
            return 5
        case "WTR":
            return 5
        case "Cold":
            return 6
        case "CL":
            return 6
        case "Acid":
            return 7
        case "AD":
            return 7
        case "Light":
            return 8
        case "LT":
            return 8
        case "Dark":
            return 9
        case "DK":
            return 9
        case "Necrotic":
            return 10
        case "NCT":
            return 10
        case "Arcane":
            return 11
        case "AC":
            return 11
        case "Existence":
            return 12
        case "EXS":
            return 12
        case _:
            return -1

#Status effect subsystem
class StatusEffect:
    def __init__(self, type_id, stacks, infinite):
        self.type = type_id
        self.stacks = stacks
        self.infinite = infinite
    @abstractmethod
    def tick(self, creature):
        if not self.infinite:
            self.stacks -= 1

def lookup_status_effect_id(string):
    match string:
        case "Bleed":
            return 0
        case "Stun":
            return 1
        case "Burning":
            return 2
        case "Suffocation":
            return 3
        case "Frozen":
            return 4
        case "Blindness":
            return 5
        case "Rot":
            return 6
        case "Manadrain":
            return 7
        case "Nonexistence":
            return 8
        case "Poison":
            return 9
        case "Fear":
            return 10
        case "Confusion":
            return 11
        case "Mindbreak":
            return 12
        case "Bloodsiphon":
            return 13
        case "Midas Curse":
            return 14
        case "Death":
            return 15
        case "Regeneration":
            return 16
        case "Berserk":
            return 17
        case "Flight":
            return 18
        case "Luck":
            return 19
        case "Ironskin":
            return 20
        case "Agility":
            return 21
        case _:
            return -1

def lookup_crit_status_effect(type_id):
    match type_id:
        case 0:
            return 0
        case 1:
            return 0
        case 2:
            return 1
        case 3:
            return 2
        case 4:
            return 2
        case 5:
            return 3
        case 6:
            return 4
        case 8:
            return 5
        case 9:
            return 5
        case 10:
            return 6
        case 11:
            return 7
        case 12:
            return 8
        case _:
            return -1

#skill subsystem, skills are represented by a tuple of integers, use the following methods to figure out the indexes of specific skills
def lookup_skill_id(string):
    match string:
        case "One-Handed Blades":
            return 0
        case "One-Handed Blade":
            return 0
        case "One-Handed Axes":
            return 1
        case "One-Handed Axe":
            return 1
        case "One-Handed Maces":
            return 2
        case "One-Handed Mace":
            return 2
        case "Two-Handed Blades":
            return 3
        case "Two-Handed Blade":
            return 3
        case "Two-Handed Axes":
            return 4
        case "Two-Handed Axe":
            return 4
        case "Two-Handed Maces":
            return 5
        case "Two-Handed Mace":
            return 5
        case "Polearms":
            return 6
        case "Polearm":
            return 6
        case "Slings":
            return 7
        case "Sling":
            return 7
        case "Bows":
            return 8
        case "Bow":
            return 8
        case "Elementalism":
            return 9
        case "Elemental":
            return 9
        case "Cursing":
            return 10
        case "Curse":
            return 10
        case "Enhancement":
            return 11
        case "Summoning":
            return 12
        case "Summon":
            return 12
        case "Transmutation":
            return 12
        case "Transmute":
            return 12
        case "Dual-Wielding":
            return 13
        case "Memory":
            return 14
        case "Search":
            return 15
        case "Hide":
            return 16
        case "Lockpicking":
            return 17
        case "Lockpick":
            return 17
        case "Disarm Trap":
            return 18
        case "Disarm":
            return 18
        case _:
            return -1

#equipment subsystem
class Equipment:
    def __init__(self, right_hand, left_hand, head, torso, legs, feet, hands, neck, finger_one, finger_two):
        self.right_hand = right_hand
        self.left_hand = left_hand
        self.head = head
        self.torso = torso
        self.legs = legs
        self.feet = feet
        self.hands = hands
        self.neck = neck
        self.finger_one = finger_one
        self.finger_two = finger_two