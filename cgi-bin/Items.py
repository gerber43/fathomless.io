#!/usr/bin/python3
import random
import sys
import cgi
from GameObject import Item, Consumable, Equippable, Weapon, TwoHandedWeapon, Smear, LightSourceItem
from SubSystem import lookup_damage_type_id, lookup_skill_id
from ActiveAbilities import Spell, Technique, HealingTouch, CreateWater, Flay, FireBolt, DarkShroud, WickedRend, \
    LightningBolt, ForceBolt, HolyBolt, DarkBolt, AcidBolt, DeathBolt, ArcaneBolt, VoidBolt, Fireball, PoisonCloud, \
    ChaosStorm, DecayCurse, MundaneCurse, ReduceAilment, Metallicize, KnitFlesh, Levitate, CleanseAilment, \
    ExpungeAilments, SuperiorMaterial
from StatusEffects import Bleed, Poison, Burning, Rot, Manaburn
from Enchantment import random_enchantment

#list of spawnable items, the name, their level, and their type
items = [("IronDagger", 1, "Weapon"), ("IronShortsword", 1, "Weapon"), ("IronGreatsword", 1, "Weapon"), ("IronHatchet", 1, "Weapon"), ("IronGreataxe", 1, "Weapon"), ("WoodenClub", 1, "Weapon"), ("WoodenGreatclub", 1, "Weapon"), ("IronSpear", 1, "Weapon"), ("IronHalberd", 1, "Weapon"), ("Sling", 1, "Weapon"), ("OakShortbow", 1, "Weapon"), ("OakLongbow", 1, "Weapon"), ("WoodenBuckler", 1, "Equippable"), ("Bandage", 1, "Consumable"), ("Pebble", 1, "Item"), ("FireBoltScroll", 1, "Consumable"), ("IceBoltScroll", 1, "Consumable"),
         ("LeatherCuirass", 2, "Equippable"), ("LeatherHelmet", 2, "Equippable"), ("LeatherBoots", 2, "Equippable"), ("LesserHealth", 2, "Consumable"), ("LesserMana", 2, "Consumable"), ("Antidote", 2, "Consumable"), ("MinorPoison", 2, "Consumable"), ("DiseasedBlood", 2, "Consumable"), ("HungryFluid", 2, "Consumable"), ("Arrow", 2, "Item"), ("FlayScroll", 2, "Consumable"),
         ("LightningBoltScroll", 3, "Consumable"), ("ForceBoltScroll", 3, "Consumable"), ("HolyBoltScroll", 3, "Consumable"), ("DarkBoltScroll", 3, "Consumable"), ("HealingTouchScroll", 3, "Consumable"),
         ("SoftWhetstone", 4, "Consumable"), ("DilutedOil", 4, "Consumable"),
         ("SteelDagger", 5, "Weapon"), ("SteelShortsword", 5, "Weapon"), ("SteelGreatsword", 5, "Weapon"), ("SteelAxe", 5, "Weapon"), ("SteelGreataxe", 5, "Weapon"), ("SteelMace", 5, "Weapon"), ("SteelGreatmaul", 5, "Weapon"), ("SteelSpear", 5, "Weapon"), ("SteelHalberd", 5, "Weapon"), ("YewShortbow", 5, "Weapon"), ("YewLongbow", 5, "Weapon"), ("SteelShield", 5, "Equippable"), ("AcidBoltScroll", 5, "Consumable"), ("DeathBoltScroll", 5, "Consumable"), ("FireballScroll", 5, "Consumable"), ("DecayCurseScroll", 5, "Consumable"), ("ReduceAilmentScroll", 5, "Consumable"),
         ("MediumPoison", 6, "Consumable"), ("RottenBlood", 6, "Consumable"), ("RavenousFluid", 6, "Consumable"), ("CreateWaterScroll", 6, "Consumable"),
         ("SteelBreastplate", 7, "Equippable"), ("SteelGreaves", 7, "Equippable"), ("SteelHelmet", 7, "Equippable"), ("SteelBoots", 7, "Equippable"), ("MedHealth", 7, "Consumable"), ("MedMana", 7, "Consumable"), ("ArcaneBoltScroll", 7, "Consumable"),
         ("PoisonCloudScroll", 8, "Consumable"), ("Metallicize", 8, "Consumable"),
         ("DarkShroudScroll", 9, "Consumable"), ("WickedRendScroll", 9, "Consumable"),
         ("MithrilDagger", 10, "Weapon"), ("MithrilShortsword", 10, "Weapon"), ("MithrilGreatsword", 10, "Weapon"), ("MithrilAxe", 10, "Weapon"), ("MithrilGreataxe", 10, "Weapon"), ("MithrilMace", 10, "Weapon"), ("MithrilGreatmaul", 10, "Weapon"), ("MithrilSpear", 10, "Weapon"), ("MithrilHalberd", 10, "Weapon"), ("SilverwoodShortbow", 10, "Weapon"), ("SilverwoodLongbow", 10, "Weapon"), ("MithrilShield", 10, "Equippable"), ("Whetstone", 10, "Consumable"), ("Oil", 10, "Consumable"), ("VoidBoltScroll", 10, "Consumable"), ("MundaneCurseScroll", 10, "Consumable"),
         ("MithrilBreastplate", 12, "Equippable"), ("MithrilGreaves", 12, "Equippable"), ("MithrilHelmet", 12, "Equippable"), ("MithrilBoots", 12, "Equippable"), ("DeadlyPoison", 12, "Consumable"), ("UndeadEssence", 12, "Consumable"), ("AntiMana", 12, "Consumable"), ("KnitFleshScroll", 12, "Consumable"),
         ("AdamantineDagger", 15, "Weapon"), ("AdamantineShortsword", 15, "Weapon"), ("AdamantineGreatsword", 15, "Weapon"), ("AdamantineAxe", 15, "Weapon"), ("AdamantineGreataxe", 15, "Weapon"), ("AdamantineMace", 15, "Weapon"), ("AdamantineGreatmaul", 15, "Weapon"), ("AdamantineSpear", 15, "Weapon"), ("AdamantineHalberd", 15, "Weapon"), ("SkywoodShortbow", 15, "Weapon"), ("SkywoodLongbow", 15, "Weapon"), ("AdamantineShield", 15, "Equippable"), ("GreaterHealth", 15, "Consumable"), ("GreaterMana", 15, "Consumable"), ("HardWhetstone", 15, "Consumable"), ("VolatileOil", 15, "Consumable"), ("ChaosStormScroll", 15, "Consumable"), ("LevitateScroll", 15, "Consumable"),
         ("AdamantineBreastplate", 17, "Equippable"), ("AdamantineGreaves", 17, "Equippable"), ("AdamantineHelmet", 17, "Equippable"), ("AdamantineBoots", 17, "Equippable"), ("CleanseAilmentScroll", 17, "Consumable"),
         ("ExpungeAilmentsScroll", 20, "Consumable"), ("SuperiorMaterialScroll", 20, "Consumable"),]

#function to pick a random item
def random_item(pos, depth):
    global items
    end_index = -1
    for i in range(len(items)):
        if items[i][1] > depth:
            end_index = i - 1
            break
    if end_index == -1:
        end_index = len(items)
    item = items[random.randint(0, end_index - 1)]
    if item[2] == "Weapon":
        #return eval(item[0])(pos, random_enchantment(item[1], True, depth))
        return eval(item[0])(pos, None)
    if item[2] == "Equippable":
        # TODO: Create at least 21 non-weapon enchantments and re-enable this code
        # return eval(item[0])(pos, random_enchantment(item[1], False, depth))
        return eval(item[0])(pos, None)
    amount = depth // item[1]
    item_prelim = eval(item[0])(pos, 0)
    if amount > item_prelim.max_stack:
        amount = item_prelim.max_stack
    return eval(item[0])(pos, amount)



#player-usable items
class Pebble(Item):
    def __init__(self, pos, amount):
        super().__init__("Pebble", "17", pos, amount, 16, 1, 0)
class Arrow(Item):
    def __init__(self, pos, amount):
        super().__init__("Arrow", "17", pos, amount, 16, 2, 5)

class Torch(LightSourceItem):
    def __init__(self, pos):
        super().__init__("Torch", 17, pos, 1, 30, "Hands", 32)

class LesserHealth(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Lesser Health Potion", "40", pos, amount, 4, 2, 20)
    def use_effect(self, grid, target):
        target.heal(target.max_hp*0.1)

class MedHealth(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Health Potion", "40", pos, amount, 4, 7, 80)
    def use_effect(self, grid, target):
        target.heal(target.max_hp*0.25)

class GreaterHealth(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Greater Health Potion", "40", pos, amount, 4, 15, 150)
    def use_effect(self, grid, target):
        target.heal(target.max_hp*0.5)

class LesserMana(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Lesser Mana Potion", "40", pos, amount, 4, 2, 20)
    def use_effect(self, grid, target):
        target.mp += int(target.max_mp*0.1)

class MedMana(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Mana Potion", "40", pos, amount, 4, 7, 80)
    def use_effect(self, grid, target):
        target.mp += int(target.max_mp*0.25)

class GreaterMana(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Greater Mana Potion", "40", pos, amount, 4, 15, 150)
    def use_effect(self, grid, target):
        target.mp += int(target.max_mp*0.5)

class Bandage(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Bandage", "40", pos, amount, 16, 1, 5)
    def use_effect(self, grid, target):
        target.heal(0)

class Antidote(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Antidote", "40", pos, amount, 16, 2, 20)
    def use_effect(self, grid, target):
        for status in target.status_effects:
            if status.status_type == "Poison":
                target.status_effects.remove(status)
                break

class Ore(Item):
    def __init__(self, pos, amount):
        super().__init__("Ore", "17", pos, amount, 10, 1, 10)

class Corruptite(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Corruptite Dust", "17", pos, amount, 5, 3, 20)
    #TODO: implement buffs and addiction

class Amulet(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Amulet", "17", pos, 0, 0, 1, "Neck", enchantment)

class Ring(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Amulet", "17", pos, 1, 15, 1, "Fingers", enchantment)

#tier 1 weapons

class IronDagger(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Dagger", "17", pos, 1, 5, 1, "One-Handed Blade", 1, 3,
                         [(lookup_damage_type_id("Piercing"), 3, 1)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class IronShortsword(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Shortsword", "17", pos, 1, 10, 3, "One-Handed Blade", 1, 1.5,
                         [(lookup_damage_type_id("Slashing"), 5, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class IronGreatsword(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Greatsword", "17", pos, 1, 30, 10, "Two-Handed Blade", 1, 2,
                         [(lookup_damage_type_id("Slashing"), 10, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class IronHatchet(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Hatchet", "17", pos, 1, 10, 5, "One-Handed Axe", 1, 1.75,
                         [(lookup_damage_type_id("Slashing"), 5, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class IronGreataxe(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Greataxe", "17", pos, 1, 30, 15, "Two-Handed Axe", 1, 2.25,
                         [(lookup_damage_type_id("Slashing"), 10, 8)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class WoodenClub(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Wooden Club", "43", pos, 1, 1, 15, "One-Handed Mace", 1, 1.5,
                         [(lookup_damage_type_id("Blunt"), 5, 0)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class WoodenGreatclub(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Wooden Greatclub", "17", pos, 1, 1, 20, "Two-Handed Mace", 1, 1.25,
                         [(lookup_damage_type_id("Blunt"), 10, 0)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class IronSpear(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Spear", "17", pos, 1, 15, 5, "Polearm", 2, 1.25,
                         [(lookup_damage_type_id("Piercing"), 3, 1)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class IronHalberd(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Iron Halberd", "17", pos, 1, 30, 15, "Polearm", 2, 1.25,
                         [(lookup_damage_type_id("Piercing"), 5, 1), (lookup_damage_type_id("Slashing"), 5, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class Sling(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Sling", "17", pos, 1, 15, 5, "Sling", 5, 1.5,
                         [(lookup_damage_type_id("Blunt"), 3, 1)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class OakShortbow(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Oak Shortbow", "17", pos, 1, 15, 3, "Bow", 5, 2,
                         [(lookup_damage_type_id("Piercing"), 5, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class OakLongbow(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Oak Longbow", "17", pos, 1, 30, 7, "Bow", 9, 2,
                         [(lookup_damage_type_id("Piercing"), 5, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

#Tier 2 Weapons

class SteelDagger(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Dagger", "17", pos, 5, 50, 1, "One-Handed Blade", 1, 3,
                         [(lookup_damage_type_id("Piercing"), 6, 1)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class SteelShortsword(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Shortsword", "17", pos, 5, 100, 3, "One-Handed Blade", 1, 1.5,
                         [(lookup_damage_type_id("Slashing"), 10, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class SteelGreatsword(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Greatsword", "17", pos, 5, 300, 10, "Two-Handed Blade", 1, 2,
                         [(lookup_damage_type_id("Slashing"), 20, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class SteelAxe(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Hatchet", "17", pos, 5, 100, 5, "One-Handed Axe", 1, 1.75,
                         [(lookup_damage_type_id("Slashing"), 10, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class SteelGreataxe(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Greataxe", "17", pos, 5, 300, 15, "Two-Handed Axe", 1, 2.25,
                         [(lookup_damage_type_id("Slashing"), 20, 8)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class SteelMace(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Mace", "43", pos, 5, 50, 15, "One-Handed Mace", 1, 1.5,
                         [(lookup_damage_type_id("Blunt"), 10, 0)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class SteelGreatmaul(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Greatmaul", "17", pos, 5, 50, 20, "Two-Handed Mace", 1, 1.25,
                         [(lookup_damage_type_id("Blunt"), 20, 0)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class SteelSpear(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Spear", "17", pos, 5, 150, 5, "Polearm", 2, 1.25,
                         [(lookup_damage_type_id("Piercing"), 6, 1)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class SteelHalberd(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Halberd", "17", pos, 5, 300, 15, "Polearm", 2, 1.25,
                         [(lookup_damage_type_id("Piercing"), 10, 1), (lookup_damage_type_id("Slashing"), 5, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class YewShortbow(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Yew Shortbow", "17", pos, 5, 150, 3, "Bow", 5, 2,
                         [(lookup_damage_type_id("Piercing"), 10, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class YewLongbow(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Yew Longbow", "17", pos, 5, 300, 7, "Bow", 9, 2,
                         [(lookup_damage_type_id("Piercing"), 10, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

#Tier 3 Weapons

class MithrilDagger(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Dagger", "17", pos, 10, 500, 1, "One-Handed Blade", 1, 3,
                         [(lookup_damage_type_id("Piercing"), 9, 1)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class MithrilShortsword(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Shortsword", "17", pos, 10, 1000, 3, "One-Handed Blade", 1, 1.5,
                         [(lookup_damage_type_id("Slashing"), 15, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class MithrilGreatsword(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Greatsword", "17", pos, 10, 3000, 10, "Two-Handed Blade", 1, 2,
                         [(lookup_damage_type_id("Slashing"), 30, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class MithrillAxe(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Hatchet", "17", pos, 10, 1000, 5, "One-Handed Axe", 1, 1.75,
                         [(lookup_damage_type_id("Slashing"), 15, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class MithrilGreataxe(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Greataxe", "17", pos, 10, 3000, 15, "Two-Handed Axe", 1, 2.25,
                         [(lookup_damage_type_id("Slashing"), 30, 8)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class MithrilMace(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Mace", "43", pos, 10, 500, 15, "One-Handed Mace", 1, 1.5,
                         [(lookup_damage_type_id("Blunt"), 15, 0)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class MithrilGreatmaul(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Greatmaul", "17", pos, 10, 500, 20, "Two-Handed Mace", 1, 1.25,
                         [(lookup_damage_type_id("Blunt"), 30, 0)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class MithrilSpear(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Spear", "17", pos, 10, 1500, 5, "Polearm", 2, 1.25,
                         [(lookup_damage_type_id("Piercing"), 9, 1)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class MithrilHalberd(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Halberd", "17", pos, 10, 3000, 15, "Polearm", 2, 1.25,
                         [(lookup_damage_type_id("Piercing"), 15, 1), (lookup_damage_type_id("Slashing"), 7, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class SilverwoodShortbow(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Silverwood Shortbow", "17", pos, 10, 1500, 3, "Bow", 5, 2,
                         [(lookup_damage_type_id("Piercing"), 15, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class SilverwoodLongbow(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Silverwood Longbow", "17", pos, 10, 3000, 7, "Bow", 9, 2,
                         [(lookup_damage_type_id("Piercing"), 15, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

#Tier 4 Weapons

class AdamantineDagger(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Adamantine Dagger", "17", pos, 15, 5000, 1, "One-Handed Blade", 1, 3,
                         [(lookup_damage_type_id("Piercing"), 12, 1)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class AdamantineShortsword(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Adamantine Shortsword", "17", pos, 15, 10000, 3, "One-Handed Blade", 1, 1.5,
                         [(lookup_damage_type_id("Slashing"), 20, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class AdamantineGreatsword(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Adamantine Greatsword", "17", pos, 15, 30000, 10, "Two-Handed Blade", 1, 2,
                         [(lookup_damage_type_id("Slashing"), 40, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class AdamantineAxe(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Adamantine Hatchet", "17", pos, 15, 10000, 5, "One-Handed Axe", 1, 1.75,
                         [(lookup_damage_type_id("Slashing"), 20, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class AdamantineGreataxe(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Adamantine Greataxe", "17", pos, 15, 30000, 15, "Two-Handed Axe", 1, 2.25,
                         [(lookup_damage_type_id("Slashing"), 40, 8)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class AdamantineMace(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Mace", "43", pos, 15, 5000, 15, "One-Handed Mace", 1, 1.5,
                         [(lookup_damage_type_id("Blunt"), 20, 0)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class AdamantineGreatmaul(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Adamantine Greatmaul", "17", pos, 15, 5000, 20, "Two-Handed Mace", 1, 1.25,
                         [(lookup_damage_type_id("Blunt"), 40, 0)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class AdamantineSpear(Weapon):
    def __init__(self, pos, enchantment):
        super().__init__("Adamantine Spear", "17", pos, 15, 15000, 5, "Polearm", 2, 1.25,
                         [(lookup_damage_type_id("Piercing"), 12, 1)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class AdamantineHalberd(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Adamantine Halberd", "17", pos, 15, 30000, 15, "Polearm", 2, 1.25,
                         [(lookup_damage_type_id("Piercing"), 20, 1), (lookup_damage_type_id("Slashing"), 10, 4)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class SkywoodShortbow(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Skywood Shortbow", "17", pos, 15, 15000, 3, "Bow", 5, 2,
                         [(lookup_damage_type_id("Piercing"), 20, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

class SkywoodLongbow(TwoHandedWeapon):
    def __init__(self, pos, enchantment):
        super().__init__("Skywood Longbow", "17", pos, 15, 30000, 7, "Bow", 9, 2,
                         [(lookup_damage_type_id("Piercing"), 20, 2)], [], enchantment)
    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)

#level 1 armor

class WoodenBuckler(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Wooden Buckler", "42", pos, 1, 10, 3, "Hands", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.02
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.04

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.02
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.04

#level 2 armor

class LeatherCuirass(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Leather Cuirass", "42", pos, 2, 15, 7, "Torso", enchantment)
    def on_equip(self, grid, equipped_creature):
        
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.3
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.07
    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.3
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.07


class LeatherSkullcap(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Leather Skullcap", "42", pos, 2, 5, 2, "Head", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.01
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.02

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.01
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.02

class LeatherBoots(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Leather Boots", "42", pos, 2, 5, 2, "Feet", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.01
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.02

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.01
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.02

#level 5 armor

class SteelShield(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Shield", "42", pos, 5, 100, 25, "Hands", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.075
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.1125

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.075
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.1125


# level 7 armor

class SteelBreastplate(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Breastplate", "42", pos, 7, 150, 30, "Torso", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.15
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.175

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.15
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.175

class SteelGreaves(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Greaves", "42", pos, 7, 120, 25, "legs", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.075
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.1125

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.075
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.1125


class SteelHelmet(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Helmet", "42", pos, 7, 50, 15, "Head", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.05
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.075

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.05
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.075


class SteelBoots(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Steel Boots", "42", pos, 7, 50, 15, "Feet", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.05
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.075

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.05
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.075


# level 10 armor

class MithrilShield(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Shield", "42", pos, 10, 1000, 25, "Hands", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.125
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.15

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.125
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.15


# level 12 armor

class MithrilBreastplate(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Breastplate", "42", pos, 12, 1500, 30, "Torso", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.2
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.25

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.2
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.25


class MithrilGreaves(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Greaves", "42", pos, 12, 1200, 25, "legs", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.125
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.15

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.125
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.15


class MithrilHelmet(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Helmet", "42", pos, 12, 500, 15, "Head", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.075
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.1

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.075
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.1


class MithrilBoots(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Mithril Boots", "42", pos, 12, 500, 15, "Feet", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.075
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.1

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.075
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.1

# level 15 armor

class AdamantineShield(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Adamantine Shield", "42", pos, 15, 10000, 25, "Hands", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.175
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.2

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.175
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.2


# level 17 armor

class AdamantineBreastplate(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Adamantine Breastplate", "42", pos, 17, 15000, 30, "Torso", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.25
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.3

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.25
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.3


class AdamantineGreaves(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Adamantine Greaves", "42", pos, 17, 12000, 25, "legs", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.175
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.2

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.175
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.2


class AdamantineHelmet(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Adamantine Helmet", "42", pos, 17, 5000, 15, "Head", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.1
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.125

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.1
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.125


class AdamantineBoots(Equippable):
    def __init__(self, pos, enchantment):
        super().__init__("Adamantine Boots", "42", pos, 17, 5000, 15, "Feet", enchantment)

    def on_equip(self, grid, equipped_creature):
        super().on_equip(grid, equipped_creature)
        equipped_creature.damage_resistances = list(equipped_creature.damage_resistances)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] += 0.1
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] += 0.125

    def on_unequip(self, grid, equipped_creature):
        super().on_unequip(grid, equipped_creature)
        (equipped_creature.damage_resistances)[lookup_damage_type_id("PRC")] -= 0.1
        (equipped_creature.damage_resistances)[lookup_damage_type_id("SLH")] -= 0.125

#scrolls

class FireBoltScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Fire Bolt", "41", pos, amount, 1, 1, 100)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(FireBolt())

class IceBoltScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Ice Bolt", "41", pos, amount, 1, 1, 100)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(FireBolt())

class FlayScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Flay", "41", pos, amount, 1, 2, 200)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(Flay())

class LightningBoltScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Lightning Bolt", "41", pos, amount, 1, 3, 300)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(LightningBolt())

class ForceBoltScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Force Bolt", "41", pos, amount, 1, 3, 300)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(ForceBolt())

class HolyBoltScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Holy Bolt", "41", pos, amount, 1, 3, 300)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(HolyBolt())

class DarkBoltScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Dark Bolt", "41", pos, amount, 1, 3, 300)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(DarkBolt())

class HealingTouchScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Healing Touch", "41", pos, amount, 1, 3, 300)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(HealingTouch())

class AcidBoltScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Acid Bolt", "41", pos, amount, 1, 5, 500)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(AcidBolt())

class DeathBoltScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Death Bolt", "41", pos, amount, 1, 5, 500)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(DeathBolt())

class FireballScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Fireball", "41", pos, amount, 1, 5, 500)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(Fireball())

class DecayCurseScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Curse of Decay", "41", pos, amount, 1, 5, 500)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(DecayCurse())

class ReduceAilmentScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Reduce Ailment", "41", pos, amount, 1, 5, 500)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(ReduceAilment())

class CreateWaterScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Create Water", "41", pos, amount, 1, 6, 600)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(CreateWater())

class ArcaneBoltScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Arcane Bolt", "41", pos, amount, 1, 7, 700)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(ArcaneBolt())

class PoisonCloudScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Poison Cloud", "41", pos, amount, 1, 8, 800)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(PoisonCloud())

class MetallicizeScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Metallicize", "41", pos, amount, 1, 8, 800)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(Metallicize())

class DarkShroudScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Create Water", "41", pos, amount, 1, 9, 900)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(DarkShroud())

class WickedRendScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Wicked Rend", "41", pos, amount, 1, 9, 900)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(WickedRend())

class VoidBoltScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Void Bolt", "41", pos, amount, 1, 10, 1000)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(VoidBolt())

class MundaneCurseScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Curse of Mundanity", "41", pos, amount, 1, 10, 1000)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(MundaneCurse())

class KnitFleshScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Curse of Knit Flesh", "41", pos, amount, 1, 12, 1200)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(KnitFlesh())

class ChaosStormScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Chaos Storm", "41", pos, amount, 1, 15, 1500)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(ChaosStorm())

class LevitateScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Levitate", "41", pos, amount, 1, 15, 1500)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(Levitate())

class CleanseAilmentScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Cleanse Ailment", "41", pos, amount, 1, 17, 1700)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(CleanseAilment())

class ExpungeAilmentsScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Expunge Ailments", "41", pos, amount, 1, 20, 2000)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(ExpungeAilments())

class SuperiorMaterialScroll(Consumable):
    def __init__(self, pos, amount):
        super().__init__("Scroll of Superior Material", "41", pos, amount, 1, 20, 2000)
    def use_effect(self, grid, target):
        total_spells_techniques = 0
        for active_ability in target.abilities:
            if isinstance(active_ability, Spell) or isinstance(active_ability, Technique):
                total_spells_techniques += 1
        if total_spells_techniques >= target.skills[lookup_skill_id("Memory")]:
            return -1
        target.abilities.append(SuperiorMaterial())

#smears

class MinorPoison(Smear):
    def __init__(self, pos, amount):
        super().__init__("Minor Poison", "17", pos, amount, 4, 2, 50, Poison(3, False))

class MediumPoison(Smear):
    def __init__(self, pos, amount):
        super().__init__("Poison", "17", pos, amount, 4, 6, 200, Poison(6, False))

class DeadlyPoison(Smear):
    def __init__(self, pos, amount):
        super().__init__("Deadly Poison", "17", pos, amount, 4, 12, 500, Poison(9, False))

class SoftWhetstone(Smear):
    def __init__(self, pos, amount):
        super().__init__("Soft Whetstone", "17", pos, amount, 2, 4, 70, Bleed(2, False))

class Whetstone(Smear):
    def __init__(self, pos, amount):
        super().__init__("Whetstone", "17", pos, amount, 2, 10, 250, Bleed(4, False))

class HardWhetstone(Smear):
    def __init__(self, pos, amount):
        super().__init__("Hard Whetstone", "17", pos, amount, 2, 15, 700, Bleed(6, False))

class DilutedOil(Smear):
    def __init__(self, pos, amount):
        super().__init__("Diluted Oil", "17", pos, amount, 2, 4, 70, Burning(2, False))

class Oil(Smear):
    def __init__(self, pos, amount):
        super().__init__("Oil", "17", pos, amount, 2, 10, 250, Burning(4, False))

class VolatileOil(Smear):
    def __init__(self, pos, amount):
        super().__init__("Volatile Oil", "17", pos, amount, 2, 15, 700, Burning(6, False))

class DiseasedBlood(Smear):
    def __init__(self, pos, amount):
        super().__init__("Diseased Blood", "17", pos, amount, 2, 2, 50, Rot(2, False))

class RottenBlood(Smear):
    def __init__(self, pos, amount):
        super().__init__("Rotten Blood", "17", pos, amount, 2, 6, 200, Rot(4, False))

class UndeadEssence(Smear):
    def __init__(self, pos, amount):
        super().__init__("Essence of Undeath", "17", pos, amount, 2, 12, 500, Rot(6, False))

class HungryFLuid(Smear):
    def __init__(self, pos, amount):
        super().__init__("Mana-Hungry Fluid", "17", pos, amount, 2, 2, 50, Manaburn(2, False))

class RavenousFluid(Smear):
    def __init__(self, pos, amount):
        super().__init__("Mana-Ravenous Fluid", "17", pos, amount, 2, 6, 200, Manaburn(4, False))

class AntiMana(Smear):
    def __init__(self, pos, amount):
        super().__init__("Anti-Mana", "17", pos, amount, 2, 12, 500, Manaburn(6, False))
