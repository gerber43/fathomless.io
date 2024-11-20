#!/usr/bin/python3
import sys
import cgi
import math
import random
from abc import abstractmethod
from GameObject import Weapon, Equippable
from SubSystem import *
from Terrain import Water, DeepWater, Fire
from Decor import Corpse
from Enchantment import random_enchantment

#Active ability base classes
class ActiveAbility:
    def __init__(self, name, textureIndex, level, cooldown, mp_cost, range, requirement):
        self.name = name
        self.textureIndex = textureIndex
        self.level = level
        self.cooldown = cooldown
        self.turns_left = 0
        self.mp_cost = mp_cost
        self.range = range
        self.requirement = requirement
    #front-end should validate that turns_left = 0 and player.mp >= mp_cost before calling use
    @abstractmethod
    def use(self, grid, caster, target):
        self.turns_left = self.cooldown

class Prayer(ActiveAbility):
    def __init__(self, name, textureIndex, level, cooldown, range):
        super().__init__(name, textureIndex, level, cooldown, range, 0, None)
    @abstractmethod
    def use(self, grid, caster, target):
        super().use(grid, caster, target)

class Spell(ActiveAbility):
    def __init__(self, name, textureIndex, level, mp_cost, range, magic_school):
        super().__init__(name, textureIndex, level, 0, mp_cost, range, magic_school)
    @abstractmethod
    def use(self, grid, caster, target):
        caster.mp -= self.mp_cost
        equip_weight = 0
        for item in caster.equipment:
            if item is not None:
                equip_weight += item.weight
        success_chance = (0.75*math.log10(float(lookup_skill_id(self.requirement))))-(0.005*equip_weight)
        failure_roll = random.random()
        if failure_roll > success_chance:
            return False
        return True

class Technique(ActiveAbility):
    def __init__(self, name, textureIndex, level, cooldown, weapon_type):
        super().__init__(name, textureIndex, level, cooldown, 0, weapon_type)
    @abstractmethod
    def use(self, grid, caster, target):
        num_hits = 0
        if isinstance(caster.equipment[0], Weapon) and caster.equipment[0].type == self.requirement:
            super().use(grid, caster, target)
            if caster.basic_attack_hit_check(grid, caster.equipment[0], isinstance(caster.equipment[1], Weapon), target):
                num_hits = num_hits + 1
        if isinstance(caster.equipment[1], Weapon) and caster.equipment[1].type == self.requirement:
            super().use(grid, caster, target)
            if caster.basic_attack_hit_check(grid, caster.equipment[1], isinstance(caster.equipment[0], Weapon), target):
                num_hits = num_hits + 1
        return num_hits

#player racial active abilities

class Blink(ActiveAbility):
    def __init__(self):
        super().__init__("Blink", "1", 0, 20, 0, 3, "")
    #target in this case is a grid location
    def use(self, grid, caster, target):
        grid[target[0]][target[1]].append(caster)
        grid[caster.pos[0]][caster.pos[1]].remove(caster)
        caster.pos = target
        super().use(grid, caster, target)

class Berserking(ActiveAbility):
    def __init__(self):
        super().__init__("Berserking", "1", 0, 50, 0, 0, "")
    def use(self, grid, caster, target):
        caster.gain_status_effect(grid, "Berserk", 20, False, False, None)
        super().use(grid, caster, target)

class Torture(ActiveAbility):
    def __init__(self):
        super().__init__("Torture", "1", 0, 30, 0, 3, "")
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "Bleed", 3, False, True, None)
        super().use(grid, caster, target)


#player-available spells

class FireBolt(Spell):
    def __init__(self):
        super().__init__("Fire Bolt", "45", 1, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Fire")))
        super().use(grid, caster, target)

class LightningBolt(Spell):
    def __init__(self):
        super().__init__("Lightning Bolt", "45", 3, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Lightning")))
        super().use(grid, caster, target)

class IceBolt(Spell):
    def __init__(self):
        super().__init__("IceB olt", "45", 1, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Cold")))
        super().use(grid, caster, target)

class HolyBolt(Spell):
    def __init__(self):
        super().__init__("Holy Bolt", "45", 3, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Light")))
        super().use(grid, caster, target)

class DarkBolt(Spell):
    def __init__(self):
        super().__init__("Dark Bolt", "45", 3, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Dark")))
        super().use(grid, caster, target)

class AcidBolt(Spell):
    def __init__(self):
        super().__init__("Acid Bolt", "45", 5, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Acid")))
        acid_destroy(grid, target, int(5*target.resistances(lookup_damage_type_id("Acid"))))
        super().use(grid, caster, target)

class DeathBolt(Spell):
    def __init__(self):
        super().__init__("Death Bolt", "45", 5, 5, 3, "Cursing")
    def use(self, grid, caster, target):
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Necrotic")))
        super().use(grid, caster, target)

class ArcaneBolt(Spell):
    def __init__(self):
        super().__init__("Arcane Bolt", "45", 7, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Arcane")))
        super().use(grid, caster, target)

class VoidBolt(Spell):
    def __init__(self):
        super().__init__("Void Bolt", "45", 10, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Existence")))
        super().use(grid, caster, target)

class CreateWater(Spell):
    def __init__(self):
        super().__init__("Create Water", "45", 6, 20, 1, "Elementalism")
    def use(self, grid, caster, target):
        grid[target[0]][target[1]].append(Water(target.pos))
        super().use(grid, caster, target)

class Fireball(Spell):
    def __init__(self):
        super().__init__("Fireball", "45", 5, 10, 5, "Elementalism")
    def use(self, grid, caster, target):
        target.hp -= int(15*target.resistances(lookup_damage_type_id("Fire")))
        for i in range(-1, 1):
            for j in range(-1, 1):
                if i == 0 and j == 0:
                    grid[target.pos[0] + i][target.pos[1] + j].append(Fire([target.pos[0] + i, target.pos[1] + j]))
        super().use(grid, caster, target)

class DecayCurse(Spell):
    def __init__(self):
        super().__init__("Curse of Decay", "45", 5, 15, 5, "Cursing")
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "Rot", 6, False, True, None)
        super().use(grid, caster, target)

class MundaneCurse(Spell):
    def __init__(self):
        super().__init__("Curse of Mundanity", "45", 10, 30, 5, "Cursing")
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "Manaburn", 10, False, True, None)
        super().use(grid, caster, target)

class HealingTouch(Spell):
    def __init__(self):
        super().__init__("Healing Touch", "45", 3, 10, 1, "Enhancement")
    def use(self, grid, caster, target):
        target.hp += 10
        super().use(grid, caster, target)

class ReduceAilment(Spell):
    def __init__(self):
        super().__init__("Reduce Ailment", "45", 5, 15, 1, "Enhancement")
    def use(self, grid, caster, target):
        for effect in target.status_effects:
            if effect.negative:
                effect.stacks -= 5
                if effect.stacks == 0:
                    target.status_effects.remove(effect)
                return
        super().use(grid, caster, target)

class Metallicize(Spell):
    def __init__(self):
        super().__init__("Metallicize", "45", 8, 20, 1, "Enhancement")
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "Ironskin", 5, False, False, None)
        super().use(grid, caster, target)

class KnitFlesh(Spell):
    def __init__(self):
        super().__init__("Knit Flesh", "45", 12, 35, 1, "Enhancement")
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "Regeneration", 10, False, False, None)
        super().use(grid, caster, target)

class Levitate(Spell):
    def __init__(self):
        super().__init__("Levitate", "45", 15, 50, 1, "Enhancement")
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "FLight", 20, False, False, None)
        super().use(grid, caster, target)

class CleanseAilment(Spell):
    def __init__(self):
        super().__init__("Cleanse Ailment", "45", 17, 80, 1, "Enhancement")
    def use(self, grid, caster, target):
        for effect in target.status_effects:
            if effect.negative:
                target.status_effects.remove()
                return
        super().use(grid, caster, target)

class ExpungeAilments(Spell):
    def __init__(self):
        super().__init__("Expunge Ailments", "45", 20, 100, 1, "Enhancement")
    def use(self, grid, caster, target):
        for effect in target.status_effects:
            if effect.negative:
                target.status_effects.remove()
        super().use(grid, caster, target)

class LesserEnchant(Spell):
    def __init__(self):
        super().__init__("Lesser Enchantment", "45", 5, 50, 1, "Enhancement")
    def use(self, grid, caster, target):
        if not isinstance(target, Equippable):
            return False
        target.enchantment = random_enchantment(0, isinstance(target, Weapon), 5)
        super().use(grid, caster, target)

class Enchant(Spell):
    def __init__(self):
        super().__init__("Enchantment", "45", 10, 100, 1, "Enhancement")
    def use(self, grid, caster, target):
        if not isinstance(target, Equippable):
            return False
        target.enchantment = random_enchantment(0, isinstance(target, Weapon), 10)
        super().use(grid, caster, target)

class GreaterEnchant(Spell):
    def __init__(self):
        super().__init__("Greater Enchantment", "45", 15, 150, 1, "Enhancement")
    def use(self, grid, caster, target):
        if not isinstance(target, Equippable):
            return False
        target.enchantment = random_enchantment(0, isinstance(target, Weapon), 15)
        super().use(grid, caster, target)

class MasterfulEnchant(Spell):
    def __init__(self):
        super().__init__("Masterful Enchantment", "45", 20, 200, 1, "Enhancement")
    def use(self, grid, caster, target):
        if not isinstance(target, Equippable):
            return False
        target.enchantment = random_enchantment(0, isinstance(target, Weapon), 15)
        super().use(grid, caster, target)

class SuperiorMaterial(Spell):
    def __init__(self):
        super().__init__("Superior Material", "45", 20, 200, 1, "Enhancement")
    def use(self, grid, caster, target):
        if not isinstance(target, Equippable):
            return False
        if target.name == "Sling":
            return
        name = target.name.split(' ')
        if name[1] == "Hatchet":
            name[1] = "Axe"
        elif name[1] == "Club":
            name[1] = "Mace"
        elif name[1] == "Greatclub":
            name[1] = "Greatmaul"
        elif name[1] == "Buckler":
            name[1] = "Shield"
        elif name[1] == "Skullcap":
            name[1] = "Helmet"
        elif name[1] == "Cuirass":
            name[1] = "Breastplate"
        if name[0] == "Mithril":
            name[0] = "Adamantine"
        elif name[0] == "Steel":
            name[0] = "Mithril"
        elif name[0] == "Wooden" or name[0] == "Iron" or name[0] == "Leather":
            name[0] = "Steel"
        new_name = name[0] + name[1]
        target = eval(new_name)(target.pos, target.enchantment)
        super().use(grid, caster, target)

#player-available techniques

#prayers

#enemy-only active abilities

class BloodBurst(ActiveAbility):
    def __init__(self):
        super().__init__("Blood Burst", "1", 0, 2, 0, 4, "")
    def use(self, grid, caster, target):
        caster.hp -= 10
        target.hp -= int(15*(1-target.resistances[lookup_damage_type_id("Dark")]))
        target.gain_status_effect(grid, "Blindness", 3, False, True, None)
        super().use(grid, caster, target)

class ShardShot(ActiveAbility):
    def __init__(self):
        super().__init__("Corruptite Shard", "1", 0, 5, 0, 5, "")
    def use(self, grid, caster, target):
        target.hp -= int(15*(1-target.resistances[lookup_damage_type_id("Piercing")]))
        target.hp -= int(15*(1-target.resistances[lookup_damage_type_id("Dark")]))
        super().use(grid, caster, target)

class FetidBreath(ActiveAbility):
    def __init__(self):
        super().__init__("Fetid Breath", "1", 0, 4, 0, 3, "")
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "Rot", 10, False, True, None)
        super().use(grid, caster, target)

class Retch(ActiveAbility):
    def __init__(self):
        super().__init__("Fetid Breath", "1", 0, 4, 0, 3, "")
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "Poison", 10, False, True, None)
        target.gain_status_effect(grid, "Rot", 10, False, True, None)
        super().use(grid, caster, target)

class Buzz(ActiveAbility):
    def __init__(self):
        super().__init__("Buzz", "1", 0, 10, 0, 10, "")
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "Confusion", 3, False, True, None)
        super().use(grid, caster, target)

#enemy-only spells

class ChokingDeep(Spell):
    def __init__(self):
        super().__init__("Choking Deep", "45", 4, 5, 7, "Cursing")
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "Suffocation", 10, False, True, None)
        super().use(grid, caster, target)

class TidalWave(Spell):
    def __init__(self):
        super().__init__("Tidal Wave", "45", 8, 20, 5, "Elementalism")
    def use(self, grid, caster, target):
        for i in range(-1, 1):
            for j in range(-1, 1):
                if i == 0 and j == 0:
                    grid[target.pos[0] + i][target.pos[1] + j].append(DeepWater([target.pos[0] + i, target.pos[1] + j]))

class Confuse(Spell):
    def __init__(self):
        super().__init__("Confuse", "45", 5, 10, 7, "Cursing")
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "Confusion", 5, False, True, None)
        super().use(grid, caster, target)

class Overwhelm(Spell):
    def __init__(self):
        super().__init__("Overwhelm", "45", 7, 15, 7, "Cursing")
    def use(self, grid, caster, target):
        target.gain_status_effect(grid, "Stun", 3, False, True, None)
        super().use(grid, caster, target)

#enemy-only techniques
