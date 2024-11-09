#!/usr/bin/python3
import sys
import cgi
import math
from abc import abstractmethod
import random
from operator import truediv
from SubSystem import *
from StatusEffects import *


class GameObject:
    def __init__(self, name, textureIndex, pos):
        self.name = name
        self.textureIndex = textureIndex
        self.pos = pos

class Item(GameObject):
    def __init__(self, name, textureIndex, pos, amount, max_stack, level, price):
        super().__init__(name, textureIndex, pos)
        self.amount = amount
        self.max_stack = max_stack
        #The item's level is a general guide for how powerful it should be
        self.level = level
        #Price the item will be sold for in shops
        self.price = price
    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.max_stack != other.max_stack:
            return False
        if self.level != other.name:
            return False
        if self.price != other.price:
            return False
        return True

class Gold(Item):
    def __init__(self, pos, amount):
        super().__init__("Gold", '7', pos, amount, 9999, 0, 1)

class Creature(GameObject):
    def __init__(self, name, textureIndex, pos, segments, hp, mp, speed, status_effects, fitness, cunning, magic, dodge,
                 crit_chance, perception, skills, equipment, abilities, damage_resistances, status_resistances,
                 inventory, inventory_size, drop_table, xp, level):
        super().__init__(name, textureIndex, pos)
        #list of creature segments, should be empty for single-tile creatures
        self.segments = segments
        self.hp = hp
        self.mp = mp
        self.max_hp = hp
        self.max_mp = mp
        self.speed = speed
        self.status_effects = status_effects
        self.fitness = fitness
        self.cunning = cunning
        self.magic = magic
        self.dodge = dodge
        self.crit_chance = crit_chance
        self.perception = perception
        self.equipment = equipment
        self.skills = skills
        self.abilities = abilities
        self.damage_resistances = damage_resistances
        self.status_resistances = status_resistances
        self.inventory = inventory
        self.inventory_size = inventory_size
        self.drop_table = drop_table
        self.xp = xp
        self.level = level

    def move(self, grid, new_pos):
        
        #for item in self.equipment:
            #if item is not None:
                #item.on_move(self, new_pos)
        grid[new_pos[0]][new_pos[1]].append(self)
        grid[self.pos[0]][self.pos[1]].remove(self)
        self.pos = new_pos
        
        #for game_object in grid[new_pos[0]][new_pos[1]]:
            
            #if isinstance(game_object, Terrain):
                #game_object.on_step(grid, self)

    def gain_status_effect(self, grid, status_type, stacks, infinite, negative, applicator):
        if negative:
            stacks = int(stacks*(1-self.status_resistances[lookup_status_resistance_id(status_type)]))
        if stacks == 0:
            return
        for status in self.status_effects:
            if status_type == status.status_type:
                if status_type == "Bloodsiphon" or status_type == "Manadrain" or status_type == "Death":
                    if status.applicator == applicator:
                        if status.infinite:
                            return
                        if infinite:
                            status.infinite = True
                            status.stacks = stacks
                            return
                        status.stacks += stacks
                        return
                    else:
                        continue
                if status.infinite:
                    return
                if infinite:
                    status.infinite = True
                    status.stacks = stacks
                    return
                status.stacks += stacks
                return
        if status_type == "Bloodsiphon" or status_type == "Manadrain" or status_type == "Death":
            new_status = eval(status_type)(stacks, infinite, applicator)
            self.status_effects.append(new_status)
            new_status.on_apply(grid, self)
            return
        elif type(status_type) is str:
            new_status = eval(status_type)(stacks, infinite)
            self.status_effects.append(new_status)
            new_status.on_apply(grid, self)

    def basic_attack_hit_check(self, grid, weapon, dual_wielding, target):
        if weapon.type == "Sling":
            found_ammo = False
            for item in self.inventory:
                if item.name == "Pebble":
                    found_ammo = True
                    item.amount = item.amount - 1
                    if item.amound <= 0:
                        self.inventory.remove(item)
            if not found_ammo:
                return False

        if weapon.type == "Bow":
            found_ammo = False
            for item in self.inventory:
                if item.name == "Arrow":
                    found_ammo = True
                    item.amount = item.amount - 1
                    if item.amound <= 0:
                        self.inventory.remove(item)
            if not found_ammo:
                return False
        
        if isinstance(target, CreatureSegment):
            target = target.creature
        
        if not isinstance(target, Creature):
            return True

        dual_penalty = 0
        if dual_wielding:
            dual_penalty = 10 - self.skills(lookup_skill_id("Dual-Wielding"))
            if dual_penalty < 0:
                dual_penalty = 0

        if isinstance(weapon, Weapon):
            hit_diff = self.skills[lookup_skill_id(weapon.type)] - target.dodge - dual_penalty
        else:
            hit_diff = weapon - target.dodge - dual_penalty
        for status in self.status_effects:
            if status.status_type == "Blindness":
                hit_diff -= status.stacks
                break
        hit_chance = 1.0 / (1.0 + (math.e ** (float(-hit_diff) / 4.0)))
        hit_roll = random.random()
        
        if hit_roll > hit_chance:
            return False
        else:
            for item in self.equipment:
                if item is not None:
                    item.on_attack(grid, self, target)
                    
            for item in target.equipment:
                if item is not None:
                    item.on_attacked(grid, target, self)
            return True

    def crit_check(self, grid):
        crit_roll = random.random()
        if crit_roll < self.crit_chance:
            return False
        else:
            return True

    def basic_attack_damage(self, grid, weapon, target, crit):
        for damage in weapon.damages:
            total = damage[1]
            if crit:
                total = total*weapon.crit_mult
            else:
                total = total + random.randint(-damage[2], damage[2])
            if (damage[0] == 0) or (damage[0] == 1) or (damage[0] == 2):
                total = total + self.fitness
                for status in self.status_effects:
                    if status.status_type == "Berserk":
                        total = total*(1+(1.0-(self.hp/self.max_hp)))
            total = int(total * (1.0-target.damage_resistances[damage[0]]))
            target.hp -= total
            if crit:
                target.gain_status_effect(grid, lookup_crit_status_effect(damage[0]), total // 10, False, True, self)
        for status in weapon.statuses:
            if isinstance(status, SmearStatus):
                target.gain_status_effect(grid, status.status_effect.status_type, status.status_effect.stacks, status.status_effect.infinite, True, self)
                status.uses_left -= 1
                if status.uses_left <= 0:
                    weapon.statuses.remove(status)
            else:
                target.gain_status_effect(grid, status.status_type, status.stacks, status.infinite, True, self)
    def basic_attack(self, grid, target):
        if isinstance(self.equipment[0], Weapon):
            if self.basic_attack_hit_check(grid, self.equipment[0], isinstance(self.equipment[1], Weapon), target):
                self.basic_attack_damage(grid, self.equipment[0], target, self.crit_check(grid))
        if isinstance(self.equipment[1], Weapon):
            if not self.basic_attack_hit_check(grid, self.equipment[1], isinstance(self.equipment[0], Weapon), target):
                self.basic_attack_damage(grid, self.equipment[1], target, self.crit_check(grid))

    def pickup_item(self, grid, target):
        grid[target.pos[0]][target.pos[1]].remove(target)
        
        for item in self.inventory:
            if target.name == item.name and item.amount + target.amount <= target.max_stack:
                item.amount += target.amount
                return
        self.inventory.append(target)


    def drop_item(self, grid, target):
        target.pos = self.pos
        grid[target.pos[0]][target.pos[1]].append(target)
        self.inventory.remove(target)

    def heal(self, amount):
        for status in self.status_effects:
            if status.status_type == "Bleed":
                self.status_effects.remove(status)
            if status.status_type == "Rot":
                amount = amount * (1.0-(status.stacks*0.05))
        amount = int(amount)
        if self.hp + amount > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp += amount

    def die(self, grid, player, corpse):
        if self == player:
            return
        if (len([gameObject for gameObject in grid[self.pos[0]][self.pos[1]] if gameObject.__class__.__base__.__name__ == "Decor"]) == 0):
            grid[self.pos[0]][self.pos[1]].append(corpse)
        for i in range(int(len(self.drop_table)/2)):
            drop_item = self.drop_table[i]
            drop_item.pos = corpse.pos
            probability = self.drop_table[i + 1]
            for status in player.status_effects:
                if status.status_type == "Luck":
                    probability = probability*1.2
                    break
            roll = random.random()
            if probability >= roll:
                grid[self.pos[0]][self.pos[1]].append(drop_item)
        player.xp += self.xp
        grid[self.pos[0]][self.pos[1]].remove(self)

class Player(Creature):
    def __init__(self, race, name, textureIndex, pos, fitness, cunning, magic, perception, abilities, damage_resistances, status_resistances):
        self.race = "Race"
        from Items import IronDagger, WoodenClub
        weapon_choice = random.randint(0, 1)
        if weapon_choice == 0:
            weapon = IronDagger((-1, -1), None)
        else:
            weapon = WoodenClub((-1, -1), None)
        super().__init__(name, textureIndex, pos, [], fitness * 10, magic * 10, 1, [], fitness, cunning, magic,
                         cunning * 2, (float(cunning) ** (2.0 / 3.0)) / 10.0, perception,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [weapon, None, None, None, None, None, None, None, None, None], abilities, damage_resistances,
                         status_resistances, [], 20, None, 0, 1)
    def check_level(self, grid):
        if self.xp >= 20*self.level:
            #TODO: display levelup screen, where player chooses to place their stat point in fitness, cunning, or magic and allocates their 5 (6 in case of human) skill points among their skills
            self.xp -= 100*self.level
            self.level += 1
            self.max_hp = self.fitness*10
            self.max_mp = self.magic*10
            self.dodge = self.cunning*2
            self.crit_chance = (float(self.cunning) ** (2.0/3.0))/10.0

#support multi-tile creatures
class CreatureSegment(GameObject):
    def __init__(self, creature, textureIndex, pos, type):
        super().__init__(creature.name, textureIndex, pos)
        self.type = type
        self.creature = creature

class Boss(Creature):
    def __init__(self, name, textureIndex, pos, segments, hp, mp, speed, status_effects, fitness, cunning, magic, dodge,
                 crit_chance, equipment, skills, abilities, damage_resistances, status_resistances, inventory,
                 inventory_size, drop_table, xp, level):
        super().__init__(name, textureIndex, pos, segments, hp, mp, speed, status_effects, fitness, cunning, magic,
                         dodge, crit_chance, 10, skills, equipment, abilities, damage_resistances, status_resistances,
                         inventory, inventory_size, drop_table, xp, level)
    def die(self, grid, player, corpse):
        if self == player:
            return
        if (len([gameObject for gameObject in grid[self.pos[0]][self.pos[1]] if gameObject.__class__.__base__.__name__ == "Decor"]) == 0):
            grid[self.pos[0]][self.pos[1]].append(corpse)
        drop_index = random.randint(0, len(self.drop_table) - 1)
        grid[self.pos[0]][self.pos[1]].append(self.drop_table[drop_index])
        player.xp += self.xp
        grid[self.pos[0]][self.pos[1]].remove(self)


class Consumable(Item):
    def __init__(self, name, textureIndex, pos, amount, max_stack, level, price):
        super().__init__(name, textureIndex, pos, amount, max_stack, level, price)
    @abstractmethod
    def use_effect(self, grid, target):
        pass

class Smear(Consumable):
    def __init__(self, name, textureIndex, pos, amount, max_stack, level, price, status_effect):
        super().__init__(name, textureIndex, pos, amount, max_stack, level, price)
        self.status_effect = status_effect
    def use_effect(self, grid, target):
        if isinstance(target.equipment[lookup_equipment_slot("Right Hand")], Weapon):
            weapon = target.equipment[lookup_equipment_slot("Right Hand")]
        elif isinstance(target.equipment[lookup_equipment_slot("Left Hand")], Weapon):
            weapon = target.equipment[lookup_equipment_slot("Left Hand")]
        else:
            return False
        weapon.statuses.append(SmearStatus(self.status_effect, target.cunning))
        return True

class Equippable(Item):
    def __init__(self, name, textureIndex, pos, level, price, weight, slot, enchantment):
        super().__init__(name, textureIndex, pos, 1, 1, level, price)
        self.weight = weight
        self.slot = slot
        self.enchantment = enchantment
        if enchantment is not None:
            self.name = self.name + " of " + enchantment.name
            self.price += enchantment.price
        self.equipped = None
    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if self.slot != other.slot:
            return False
        return True
    @abstractmethod
    def on_equip(self, grid, equipped_creature):
       chosen_slot = self.slot
       if self.slot == "Hands":
           if equipped_creature.equipment[lookup_equipment_slot("Right Hand")] is None:
               chosen_slot = "Right Hand"
           elif equipped_creature.equipment[lookup_equipment_slot("Left Hand")] is None:
               chosen_slot = "Left Hand"
           else:
               return None
       if self.slot == "Fingers":
           if equipped_creature.equipment[lookup_equipment_slot("Right Finger")] is None:
               chosen_slot = "Right Finger"
           elif equipped_creature.equipment[lookup_equipment_slot("Left Finger")] is None:
               chosen_slot = "Left Finger"
           else:
               return None
       if equipped_creature.equipment[lookup_equipment_slot(chosen_slot)] is None:
            self.equipped = chosen_slot
            equipped_creature.equipment = list(equipped_creature.equipment)
            equipped_creature.equipment[lookup_equipment_slot(chosen_slot)] = self
            equipped_creature.inventory.remove(self)
            if self.enchantment is not None:
                self.enchantment.on_equip(self, grid, equipped_creature)
            return chosen_slot
       return None
    @abstractmethod
    def on_unequip(self, grid, equipped_creature):
        if self.equipped is None:
            return None
        equipped_creature.equipment[lookup_equipment_slot(self.equipped)] = None
        self.equipped = None
        if self.enchantment is not None:
            self.enchantment.on_unequip(self, grid, equipped_creature)
        if len(equipped_creature.inventory) >= equipped_creature.inventory_size:
            self.pos = equipped_creature.pos
            grid[self.pos[0]][self.pos[1]].append(self)
        else:
            equipped_creature.inventory.append(self)
        return

    def on_move(self, grid, equipped_creature, new_pos):
        if not self.equipped:
            return False
        else:
            if self.enchantment is not None:
                self.enchantment.on_move(self, grid, equipped_creature)
            return True
    def on_attack(self, grid, equipped_creature, target):
        if not self.equipped:
            return False
        else:
            if self.enchantment is not None:
                self.enchantment.on_move(self, grid, equipped_creature)
            return True
    def on_attacked(self, grid, equipped_creature, attacker):
        if not self.equipped:
            return False
        else:
            if self.enchantment is not None:
                self.enchantment.on_move(self, grid, equipped_creature)
            return True
    def on_ability(self, grid, equipped_creature, target):
        if not self.equipped:
            return False
        else:
            if self.enchantment is not None:
                self.enchantment.on_move(self, grid, equipped_creature)
            return True

class Weapon(Equippable):
    def __init__(self, name, textureIndex, pos, level, price, weight, type, range, crit_mult, damages, statuses, enchantment):
        super().__init__(name, textureIndex, pos, level, price, weight, "Hands", enchantment)
        self.type = type
        self.range = range
        self.crit_mult = crit_mult
        self.damages = damages
        self.statuses = statuses
        if self.enchantment is not None:
            self.damages = self.damages + self.enchantment.damages
            self.statuses = self.statuses + self.enchantment.statuses
    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if self.type != other.type:
            return False
        if self.range != other.range:
            return False
        if self.damages != other.damages:
            return False
        if self.statuses != other.statuses:
            return False
        return True
    @abstractmethod
    def on_equip(self, grid, equipped_creature):
        return super().on_equip(grid, equipped_creature)
    @abstractmethod
    def on_unequip(self, grid, equipped_creature):
        return super().on_equip(grid, equipped_creature)

#When a two-handed weapon is equipped in a hand slot, this is placed in the other hand slot
class Unavailable(Equippable):
    def __init__(self):
        super().__init__("", "", (-1, -1), 0, 0, 0, "Left Hand", None)
    def on_equip(self, grid, equipped_creature):
        pass
    def on_unequip(self, grid, equipped_creature):
        pass

class TwoHandedWeapon(Weapon):
    def __init__(self, name, textureIndex, pos, level, price, weight, type, range, crit_mult, damages, statuses, enchantment):
        super().__init__(name, textureIndex, pos, level, price, weight, type, range, crit_mult, damages, statuses, enchantment)

    def on_equip(self, grid, equipped_creature):
        if equipped_creature.equipment[lookup_equipment_slot("Right Hand")] is None and equipped_creature.equipment[lookup_equipment_slot("Left Hand")] is None:
            self.equipped = "Right Hand"
            equipped_creature.equipment = list(equipped_creature.equipment)
            equipped_creature.equipment[lookup_equipment_slot("Right Hand")] = self
            equipped_creature.inventory.remove(self)
            equipped_creature.equipment[lookup_equipment_slot("Left Hand")] = Unavailable()
            if self.enchantment is not None:
                self.enchantment.on_equip(self, grid, equipped_creature)
            return "Right Hand"
        return None

    def on_unequip(self, grid, equipped_creature):
        equipped_creature.equipment[lookup_equipment_slot("Left Hand")] = None
        return super().on_unequip(grid, equipped_creature)

class Terrain(GameObject):
    def __init__(self, name, textureIndex, pos, hp, resistances, passable, block_sight, warn_flying, warning):
        super().__init__(name, textureIndex, pos)
        self.hp = hp
        self.resistances = resistances
        self.dodge = 0
        self.passable = passable
        self.block_sight = block_sight
        #warn can be NO, YES, or WALK
        self.warn_flying = warn_flying
        #message displayed when warn is triggered
        self.warning = warning
    def on_creation(self, grid):
        pass
    #onStep applies every time a creature ends its turn on the tile with this terrain
    def on_step(self, grid, creature):
        pass

class Decor(GameObject):
    def __init__(self, name, textureIndex, pos, hp, resistances, passable, block_sight, warn, warning):
        super().__init__(name, textureIndex, pos)
        self.hp = hp
        self.resistances = resistances
        self.passable = passable
        self.block_sight = block_sight
        self.dodge = 0
        #warn can be NO, YES, or WALK
        self.warn = warn
        # message displayed when warn is triggered
        self.warning = warning
    def on_interact(self, grid, creature):
        pass
    def on_destroy(self, grid):
        grid[self.pos[0]][self.pos[1]].remove(self)
    def passive_behavior(self, grid):
        pass

class Light(GameObject):
    def __init__(self, pos, level):
        super().__init__("Light", "", pos)
        self.level = level

def spread_light(grid, pos, level, touched_tiles):
    if level == 0:
        return
    for tile in touched_tiles:
        if pos == tile[0]:
            return
    light_pointer = None
    light_blocked = False
    for game_object in grid[pos[0]][pos[1]]:
        if isinstance(game_object, Light):
            light_pointer = game_object
        if isinstance(game_object, Terrain) or isinstance(game_object, Decor):
            if game_object.block_sight:
                light_blocked = True
    if not touched_tiles:
        true_level = level
    else:
        true_level = int(touched_tiles[0][1]*(0.5**manhattan(pos, touched_tiles[0][0])))
    touched_tiles.append((pos, true_level))
    if light_pointer is None:
        grid[pos[0]][pos[1]].append(Light(pos, true_level))
    else:
        light_pointer.level += level
    if light_blocked:
        return
    spread_light(grid, (pos[0]+1, pos[1]), level/2, touched_tiles)
    spread_light(grid, (pos[0]-1, pos[1]), level/2, touched_tiles)
    spread_light(grid, (pos[0], pos[1]+1), level/2, touched_tiles)
    spread_light(grid, (pos[0], pos[1]-1), level/2, touched_tiles)
    return touched_tiles

def remove_light(grid, touched_tiles):
    for tile in touched_tiles:
        for game_object in grid[tile[0][0]][tile[0][1]]:
            if isinstance(game_object, Light):
                game_object.level -= tile[1]
                if game_object.level <= 0:
                    grid[tile[0][0]][tile[0][1]].remove(game_object)
                    
class LightSourceItem(Equippable):
    def __init__(self, name, textureIndex, pos, level, price, slots, intensity):
        super().__init__(name, textureIndex, pos, level, price, slots)
        self.intensity = intensity
        self.lit_tiles = []
    def on_equip(self, grid, equipped_creature):
        if not super().on_equip(grid, equipped_creature):
            return False
        self.lit_tiles = spread_light(grid, equipped_creature.pos, self.level, [])
    def on_unequip(self, grid, equipped_creature):
        if not super().on_equip(grid, equipped_creature):
            return False
        remove_light(grid, self.lit_tiles)
        self.lit_tiles = []
    def on_move(self, grid, equipped_creature, new_pos):
        if not super().on_move(grid, equipped_creature, new_pos):
            return False
        remove_light(grid, self.lit_tiles)
        self.lit_tiles = spread_light(grid, equipped_creature.pos, self.level, [])

class LightDecor(Decor):
    def __init__(self, name, textureIndex, pos, hp, resistances, passable, warn, warning, intensity, lit):
        super().__init__(name, textureIndex, pos, hp, resistances, passable, False, warn, warning)
        self.intensity = intensity
        self.lit = lit
        if lit:
            pass
           #spread_light(grid, pos, intensity, [])
    def on_interact(self, grid, creature):
        if self.lit:
            self.lit = False
            remove_light(grid, [])
        else:
            self.lit = True
            spread_light(grid, self.pos, self.intensity, [])
    @abstractmethod
    def passive_behavior(self, grid):
        pass

class LightTerrain(Terrain):
    def __init__(self, grid, name, textureIndex, pos, hp, resistances, passable, warn_flying, warning, intensity, lit):
        super().__init__(name, textureIndex, pos, hp, resistances, passable, False, warn_flying, warning)
        self.intensity = intensity
        self.lit = lit
        if lit:
           spread_light(grid, pos, intensity, [])
    @abstractmethod
    def on_creation(self, grid):
        pass
    @abstractmethod
    def on_step(self, grid, creature):
        pass
