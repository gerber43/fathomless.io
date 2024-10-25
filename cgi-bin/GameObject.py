#!/usr/bin/python3
import sys
import cgi
import math
from abc import abstractmethod
import random
from operator import truediv
from SubSystem import *



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
                 crit_chance, equipment, skills, abilities, damage_resistances, status_resistances, inventory,
                 inventory_size, drop_table, xp, level):
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

    def gain_status_effect(self, grid, type_id, stacks, infinite):
        if stacks == 0:
            return
        for status in self.status_effects:
            if type_id == status.type_id:
                if status.infinite:
                    return
                if infinite:
                    status.infinite = True
                    status.stacks = stacks
                    return
                status.stacks += stacks
                return
        self.status_effects.append(StatusEffect(type_id, stacks, infinite))

    def basic_attack_hit_check(self, grid, weapon, target):
        #TODO: Implement ammo checking and ammo decrement
        if isinstance(target, CreatureSegment):
            target = target.creature
        if not isinstance(target, Creature):
            return True
        if isinstance(weapon, Weapon):
            hit_diff = self.skills[lookup_skill_id(weapon.type)] - target.dodge
        else:
            hit_diff = weapon - target.dodge
        hit_chance = 1.0 / (1.0 + (math.e ** (float(-hit_diff) / 4.0)))
        hit_roll = random.random
        if hit_roll > hit_chance:
            return False
        else:
            for item in self.equipment:
                if item is not None:
                    item.on_attack(self, target)
            for item in target.equipment:
                if item is not None:
                    item.on_attacked(target, self)
            return True

    def crit_check(self, grid):
        crit_roll = random.random
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
            total = int(total * (1.0-target.damage_resistances[damage[0]]))
            target.hp -= total
            if crit:
                target.gain_status_effect(lookup_crit_status_effect(damage[0]), total / 10, False)
        for status in weapon.statuses:
            target.gain_status_effect(status.type_id, status.stacks, status.infinite)
    def basic_attack(self, grid, target):
        #TODO: apply dual wielding penalty if dual wielding
        if isinstance(self.equipment[0], Weapon):
            if self.basic_attack_hit_check(grid, self.equipment[0], target):
                self.basic_attack_damage(grid, self.equipment[0], target, self.crit_check(grid))
        if isinstance(self.equipment[1], Weapon):
            if not self.basic_attack_hit_check(grid, self.equipment[1], target):
                self.basic_attack_damage(grid, self.equipment[1], target, self.crit_check(grid))

    def pickup_item(self, grid, target):
        grid[self.pos[0]][self.pos[1]].remove(target)
        for item in self.inventory:
            if target.name == item.name and item.amount + target.amount <= target.max_stack:
                item.amount += target.amount
                return
        self.inventory.append(target)


    def drop_item(self, grid, target):
        target.pos = self.pos
        grid[target.pos[0]][target.pos[1]].append(target)
        self.inventory.remove(target)

    def die(self, grid, player,corpse):
        if self == player:
            return
        grid[self.pos[0]][self.pos[1]].append(corpse)
        for i in range(int(len(self.drop_table)/2)):
            drop_item = self.drop_table[i]
            probability = self.drop_table[i + 1]
            roll = random.random()
            if probability >= roll:
                grid[self.pos[0]][self.pos[1]].append(drop_item)
        player.xp += self.xp
        grid[self.pos[0]][self.pos[1]].remove(self)

class Player(Creature):
    def __init__(self, name, textureIndex, pos, fitness, cunning, magic, abilities, damage_resistances, status_resistances):
        super().__init__(name, textureIndex, pos, (), fitness * 10, magic * 10, 1, [], fitness, cunning, magic, cunning*2, (float(cunning) ** (2.0/3.0))/10.0,
                         (None, None, None, None, None, None, None, None, None, None),
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), abilities, damage_resistances,
                         status_resistances, [], 20, None, 0, 1)
    def check_level(self, grid):
        if self.xp >= 100*self.level:
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


class Consumable(Item):
    def __init__(self, name, textureIndex, pos, amount, max_stack, level, price):
        super().__init__(name, textureIndex, pos, amount, max_stack, level, price)
    @abstractmethod
    def use_effect(self, grid, target):
        pass
    @abstractmethod
    def throw_effect(self, grid, target):
        pass

class Equippable(Item):
    def __init__(self, name, textureIndex, pos, level, price, weight, slots):
        super().__init__(name, textureIndex, pos, 1, 1, level, price)
        self.weight = weight
        self.slots = slots
        self.equipped = None
    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if self.slots != other.slots:
            return False
        return True
    @abstractmethod
    def on_equip(self, grid, equipped_creature):
        for slot in self.slots:
            if equipped_creature.equipment[lookup_equipment_slot(slot)] is None:
                self.equipped = slot
                equipped_creature.equipment[lookup_equipment_slot(slot)] = self
                equipped_creature.inventory.remove(self)
                return True
        return False
    @abstractmethod
    def on_unequip(self, grid, equipped_creature):
        if self.equipped is None:
            return False
        equipped_creature.equipment[lookup_equipment_slot(self.equipped)] = None
        self.equipped = None
        if len(equipped_creature.inventory) >= equipped_creature.inventory_size:
            self.pos = equipped_creature.pos
            grid[self.pos[0]][self.pos[1]].append(self)
        else:
            equipped_creature.inventory.append(self)

    def on_move(self, grid, equipped_creature, new_pos):
        if not self.equipped:
            return False
        else:
            return True
    def on_attack(self, grid, equipped_creature, target):
        if not self.equipped:
            return False
        else:
            return True
    def on_attacked(self, grid, equipped_creature, attacker):
        if not self.equipped:
            return False
        else:
            return True
    def on_ability(self, grid, equipped_creature, target):
        if not self.equipped:
            return False
        else:
            return True

class Weapon(Equippable):
    def __init__(self, name, textureIndex, pos, level, price, weight, type, range, crit_mult, damages, statuses, slots):
        super().__init__(name, textureIndex, pos, level, price, weight, slots)
        self.type = type
        self.range = range
        self.crit_mult = crit_mult
        self.damages = damages
        self.statuses = statuses
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
    def __init__(self, pos):
        super().__init__("", "", pos, 0, 0, 0, ("right_hand", "left_hand"))
    def on_equip(self, grid, equipped_creature):
        return super().on_equip(grid, equipped_creature)
    def on_unequip(self, grid, equipped_creature):
        return super().on_unequip(grid, equipped_creature)

class Terrain(GameObject):
    def __init__(self, name, textureIndex, pos, hp, resistances, passable, block_sight, warn, warning):
        super().__init__(name, textureIndex, pos)
        self.hp = hp
        self.resistances = resistances
        self.dodge = 0
        self.passable = passable
        self.block_sight = block_sight
        #warn can be NO, YES, or WALK
        self.warn = warn
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
    def __init__(self, grid, name, textureIndex, pos, hp, resistances, passable, warn, warning, intensity, lit):
        super().__init__(name, textureIndex, pos, hp, resistances, passable, False, warn, warning)
        self.intensity = intensity
        self.lit = lit
        if lit:
           spread_light(grid, pos, intensity, [])
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
    def __init__(self, grid, name, textureIndex, pos, hp, resistances, passable, warn, warning, intensity, lit):
        super().__init__(name, textureIndex, pos, hp, resistances, passable, False, warn, warning)
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
