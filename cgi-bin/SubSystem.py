#!/usr/bin/python3
import sys
import cgi
import math
from abc import abstractmethod

damageTypes = ["Piercing","PRC","Slashing","SLH","Blunt","BLT","Fire","FR","Lightning","LTG","Water","WTR","Cold","CL","Acid","AD","Light","LT","Dark","DK","Necrotic","NCT","Arcane","AC","Existence","EXS"]
statusEffects = ["Bleed","Stun","Burning","Suffocation","Frozen","Blindness","Rot","Manadrain","Nonexistence","Poison","Fear","Confusion","Mindbreak","Bloodsiphon","MidasCurse","Death","Regeneration","Berserk","Flight","Luck","Ironskin","Agility"]
critStatusEffects = [0,0,1,2,2,3,4,5,5,6,7,8]
skillIds = ["One-HandedBlades","One-HandedBlade","One-HandedAxes","One-HandedAxe","One-HandedMaces","One-HandedMace","Two-HandedBlades","Two-HandedBlade","Two-HandedAxes","Two-HandedAxe","Two-HandedMaces","Two-HandedMace","Polearms","Polearm","Slings","Sling","Bows","Bow","Elementalism","Elemental","Cursing","Curse","Enhancement","Enhancement","Summoning","Summon","Dual-Wielding","Dual-Wielding","Memory","Memory","Search","Search","Hide","Hide","Lockpicking","Lockpick","DisarmTrap","Disarm"]
#damage type and resistance subsystem, resistances are represented by a tuple of floats, use the following methods to figure out the indexes of specific  damage types and resistances
def lookup_damage_type_id(damageType):
    if damageType in damageTypes:
        return math.floor(damageTypes.index(damageType)/2)
    else:
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

def lookup_status_effect_id(statusEffect):
    if statusEffect in statusEffects:
        return statusEffects.index(statusEffect)
    else:
        return -1
        
def lookup_crit_status_effect(type_id):
    if type_id in critStatusEffects:
        return critStatusEffects.index(type_id)
    else:
        return -1

#skill subsystem, skills are represented by a tuple of integers, use the following methods to figure out the indexes of specific skills
def lookup_skill_id(string):
    if (string == "Transmutation" or string == "Transmute"):
        return 12
    elif string in skillIds:
        return skillIds.index(string)
    else:
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
