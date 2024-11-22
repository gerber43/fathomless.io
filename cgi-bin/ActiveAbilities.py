#!/usr/bin/python3
import sys
import cgi
import math
import random
from abc import abstractmethod
from GameObject import Weapon, Equippable, CreatureSegment, Light
from SubSystem import *
from Terrain import Water, DeepWater, Fire, PoisonFog


#from Decor import Corpse
#from Enchantment import random_enchantment

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
        if isinstance(target, CreatureSegment):
            target = target.creature
        self.turns_left = self.cooldown
        return target

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
            return None
        if isinstance(target, CreatureSegment):
            target = target.creature
        return target

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
        target = super().use(grid, caster, target)
        grid[target[0]][target[1]].append(caster)
        grid[caster.pos[0]][caster.pos[1]].remove(caster)
        caster.pos = target
        super().use(grid, caster, target)

class Berserking(ActiveAbility):
    def __init__(self):
        super().__init__("Berserking", "1", 0, 50, 0, 0, "")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        caster.gain_status_effect(grid, "Berserk", 20, False, False, None)

class Torture(ActiveAbility):
    def __init__(self):
        super().__init__("Torture", "1", 0, 30, 0, 3, "")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        target.gain_status_effect(grid, "Bleed", 3, False, True, None)


#player-available spells

class FireBolt(Spell):
    def __init__(self):
        super().__init__("Fire Bolt", "45", 1, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Fire")))

class LightningBolt(Spell):
    def __init__(self):
        super().__init__("Lightning Bolt", "45", 3, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Lightning")))

class ForceBolt(Spell):
    def __init__(self):
        super().__init__("Force Bolt", "45", 3, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Blunt")))

class IceBolt(Spell):
    def __init__(self):
        super().__init__("IceB olt", "45", 1, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Cold")))

class HolyBolt(Spell):
    def __init__(self):
        super().__init__("Holy Bolt", "45", 3, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Light")))

class DarkBolt(Spell):
    def __init__(self):
        super().__init__("Dark Bolt", "45", 3, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Dark")))

class AcidBolt(Spell):
    def __init__(self):
        super().__init__("Acid Bolt", "45", 5, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Acid")))
        acid_destroy(grid, target, int(5*target.resistances(lookup_damage_type_id("Acid"))))

class DeathBolt(Spell):
    def __init__(self):
        super().__init__("Death Bolt", "45", 5, 5, 3, "Cursing")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Necrotic")))

class ArcaneBolt(Spell):
    def __init__(self):
        super().__init__("Arcane Bolt", "45", 7, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Arcane")))

class VoidBolt(Spell):
    def __init__(self):
        super().__init__("Void Bolt", "45", 10, 5, 3, "Elementalism")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp -= int(5*target.resistances(lookup_damage_type_id("Existence")))

class CreateWater(Spell):
    def __init__(self):
        super().__init__("Create Water", "45", 6, 20, 1, "Elementalism")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        grid[target[0]][target[1]].append(Water(target.pos))

class Fireball(Spell):
    def __init__(self):
        super().__init__("Fireball", "45", 5, 10, 5, "Elementalism")
    def use(self, grid, caster, target):
        original_target = target
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp -= int(15*target.resistances(lookup_damage_type_id("Fire")))
        target = original_target
        for i in range(-1, 1):
            for j in range(-1, 1):
                if i == 0 and j == 0:
                    grid[target.pos[0] + i][target.pos[1] + j].append(Fire([target.pos[0] + i, target.pos[1] + j]))

class PoisonCloud(Spell):
    def __init__(self):
        super().__init__("Poison Cloud", "45", 8, 20, 5, "Elementalism")
    def use(self, grid, caster, target):
        if super().use(grid, caster ,target) is None:
            return False
        for i in range(-1, 1):
            for j in range(-1, 1):
                if i == 0 and j == 0:
                    grid[target.pos[0] + i][target.pos[1] + j].append(PoisonFog([target.pos[0] + i, target.pos[1] + j]))

class DarkShroud(Spell):
    def __init__(self):
        super().__init__("Dark Shroud", "45", 9, 25, 5, "Elementalism")
    def use(self, grid, caster, target):
        if super().use(grid, caster, target) is None:
            return False
        target = caster
        for i in range(-1, 1):
            for j in range(-1, 1):
                if i == 0 and j == 0:
                    for game_object in grid[target.pos[0] + i][target.pos[1] + j]:
                        if isinstance(game_object, Light):
                            game_object.intensity = 0

class WickedRend(Spell):
    def __init__(self):
        super().__init__("Wicked Rend", "45", 9, 25, 5, "Cursing")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp -= int(20 * target.resistances(lookup_damage_type_id("Dark")))
        target.gain_status_effect(grid, "Bleed", 5, False, True, None)


class ChaosStorm(Spell):
    def __init__(self):
        super().__init__("Chaos Storm", "45", 15, 150, 5, "Elementalism")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp -= int(10 * target.resistances(lookup_damage_type_id("Fire")))
        target.hp -= int(10 * target.resistances(lookup_damage_type_id("Lightning")))
        target.hp -= int(10 * target.resistances(lookup_damage_type_id("Acid")))
        acid_destroy(grid, target, int(5 * target.resistances(lookup_damage_type_id("Acid"))))

class Flay(Spell):
    def __init__(self):
        super().__init__("Flay", "45", 2, 10, 5, "Cursing")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.gain_status_effect(grid, "Bleed", 6, False, True, None)

class DecayCurse(Spell):
    def __init__(self):
        super().__init__("Curse of Decay", "45", 5, 15, 5, "Cursing")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.gain_status_effect(grid, "Rot", 6, False, True, None)

class MundaneCurse(Spell):
    def __init__(self):
        super().__init__("Curse of Mundanity", "45", 10, 30, 5, "Cursing")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.gain_status_effect(grid, "Manaburn", 10, False, True, None)

class HealingTouch(Spell):
    def __init__(self):
        super().__init__("Healing Touch", "45", 3, 10, 1, "Enhancement")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.hp += 10

class ReduceAilment(Spell):
    def __init__(self):
        super().__init__("Reduce Ailment", "45", 5, 15, 1, "Enhancement")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        for effect in target.status_effects:
            if effect.negative:
                effect.stacks -= 5
                if effect.stacks == 0:
                    target.status_effects.remove(effect)
                return

class Metallicize(Spell):
    def __init__(self):
        super().__init__("Metallicize", "45", 8, 20, 1, "Enhancement")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.gain_status_effect(grid, "Ironskin", 5, False, False, None)

class KnitFlesh(Spell):
    def __init__(self):
        super().__init__("Knit Flesh", "45", 12, 35, 1, "Enhancement")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.gain_status_effect(grid, "Regeneration", 10, False, False, None)

class Levitate(Spell):
    def __init__(self):
        super().__init__("Levitate", "45", 15, 50, 1, "Enhancement")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.gain_status_effect(grid, "FLight", 20, False, False, None)

class CleanseAilment(Spell):
    def __init__(self):
        super().__init__("Cleanse Ailment", "45", 17, 80, 1, "Enhancement")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        for effect in target.status_effects:
            if effect.negative:
                target.status_effects.remove()
                return

class ExpungeAilments(Spell):
    def __init__(self):
        super().__init__("Expunge Ailments", "45", 20, 100, 1, "Enhancement")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        for effect in target.status_effects:
            if effect.negative:
                target.status_effects.remove()

class LesserEnchant(Spell):
    def __init__(self):
        super().__init__("Lesser Enchantment", "45", 5, 50, 1, "Enhancement")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        if not isinstance(target, Equippable):
            return False
        target.enchantment = random_enchantment(0, isinstance(target, Weapon), 5)

class Enchant(Spell):
    def __init__(self):
        super().__init__("Enchantment", "45", 10, 100, 1, "Enhancement")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        if not isinstance(target, Equippable):
            return False
        target.enchantment = random_enchantment(0, isinstance(target, Weapon), 10)

class GreaterEnchant(Spell):
    def __init__(self):
        super().__init__("Greater Enchantment", "45", 15, 150, 1, "Enhancement")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        if not isinstance(target, Equippable):
            return False
        target.enchantment = random_enchantment(0, isinstance(target, Weapon), 15)

class MasterfulEnchant(Spell):
    def __init__(self):
        super().__init__("Masterful Enchantment", "45", 20, 200, 1, "Enhancement")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        if not isinstance(target, Equippable):
            return False
        target.enchantment = random_enchantment(0, isinstance(target, Weapon), 15)

class SuperiorMaterial(Spell):
    def __init__(self):
        super().__init__("Superior Material", "45", 20, 200, 1, "Enhancement")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
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

#player-available techniques

#prayers

#enemy-only active abilities

class BloodBurst(ActiveAbility):
    def __init__(self):
        super().__init__("Blood Burst", "1", 0, 2, 0, 4, "")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        caster.hp -= 10
        target.hp -= int(15*(1-target.resistances[lookup_damage_type_id("Dark")]))
        target.gain_status_effect(grid, "Blindness", 3, False, True, None)

class ShardShot(ActiveAbility):
    def __init__(self):
        super().__init__("Corruptite Shard", "1", 0, 5, 0, 5, "")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        target.hp -= int(15*(1-target.resistances[lookup_damage_type_id("Piercing")]))
        target.hp -= int(15*(1-target.resistances[lookup_damage_type_id("Dark")]))

class FetidBreath(ActiveAbility):
    def __init__(self):
        super().__init__("Fetid Breath", "1", 0, 4, 0, 3, "")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        target.gain_status_effect(grid, "Rot", 10, False, True, None)

class Retch(ActiveAbility):
    def __init__(self):
        super().__init__("Fetid Breath", "1", 0, 4, 0, 3, "")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        target.gain_status_effect(grid, "Poison", 10, False, True, None)
        target.gain_status_effect(grid, "Rot", 10, False, True, None)

class Buzz(ActiveAbility):
    def __init__(self):
        super().__init__("Buzz", "1", 0, 10, 0, 10, "")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        target.gain_status_effect(grid, "Confusion", 3, False, True, None)
#enemy-only spells

class ChokingDeep(Spell):
    def __init__(self):
        super().__init__("Choking Deep", "45", 4, 5, 7, "Cursing")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.gain_status_effect(grid, "Suffocation", 10, False, True, None)

class TidalWave(Spell):
    def __init__(self):
        super().__init__("Tidal Wave", "45", 8, 20, 5, "Elementalism")
    def use(self, grid, caster, target):
        if super().use(grid, caster, target) is None:
            return False
        for i in range(-1, 1):
            for j in range(-1, 1):
                if i == 0 and j == 0:
                    grid[target.pos[0] + i][target.pos[1] + j].append(DeepWater([target.pos[0] + i, target.pos[1] + j]))

class Confuse(Spell):
    def __init__(self):
        super().__init__("Confuse", "45", 5, 10, 7, "Cursing")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.gain_status_effect(grid, "Confusion", 5, False, True, None)

class Overwhelm(Spell):
    def __init__(self):
        super().__init__("Overwhelm", "45", 7, 15, 7, "Cursing")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.gain_status_effect(grid, "Stun", 3, False, True, None)

class Freeze(Spell):
    def __init__(self):
        super().__init__("Freeze", "45", 10, 30, 7, "Elementalism")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.gain_status_effect(grid, "Frozen", 3, False, True, None)

class Exsanguinate(Spell):
    def __init__(self):
        super().__init__("Exsanguinate", "45", 10, 30, 5, "Cursing")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.gain_status_effect(grid, "Bleed", 15, False, True, None)

class SiphonBlood(Spell):
    def __init__(self):
        super().__init__("Siphon Blood", "45", 10, 35, 5, "Cursing")
    def use(self, grid, caster, target):
        target = super().use(grid, caster, target)
        if target is None:
            return False
        target.gain_status_effect(grid, "Bloodsiphon", 5, False, True, caster)

#enemy-only techniques
