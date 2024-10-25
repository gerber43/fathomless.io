#!/usr/bin/python3
import sys
import cgi
from SubSystem import *

#negative statuses

class Bleed(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Bleed", stacks, infinite)
  def tick(self, grid, creature):
      creature.hp -= self.stacks

#TODO: Stun functionality in frontend
class Stun(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Stun", stacks, infinite)
  def tick(self, grid, creature):
      super().tick(grid, creature)

class Burning(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Burning", stacks, infinite)
  def tick(self, grid, creature):
      creature.hp -= self.stacks

class Suffocation(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Suffocation", stacks, infinite)
  def tick(self, grid, creature):
      if self.stacks >= creature.hp:
          creature.die()
      super().tick(grid, creature)

#TODO: Stun functionality in frontend
class Frozen(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Frozen", stacks, infinite)
  def tick(self, grid, creature):
      super().tick(grid, creature)

#TODO: Blindness functionality in basic_attack_hit_check
class Blindness(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Blindness", stacks, infinite)
  def tick(self, grid, creature):
      super().tick(grid, creature)

#TODO: Rot functionality in healing code
class Rot(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Rot", stacks, infinite)
  def tick(self, grid, creature):
      super().tick(grid, creature)

class Manaburn(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Manaburn", stacks, infinite)
  def tick(self, grid, creature):
      creature.mp -= self.stacks
      super().tick(grid, creature)

class Nonexistence(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Nonexistence", stacks, infinite)
  def tick(self, grid, creature):
      if self.stacks >= creature.mp:
          creature.die()
      super().tick(grid, creature)

class Poison(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Poison", stacks, infinite)
  def tick(self, grid, creature):
      creature.hp -= self.stacks
      super().tick(grid, creature)

#TODO: Fear functionality in frontend
class Fear(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Fear", stacks, infinite)
  def tick(self, grid, creature):
      super().tick(grid, creature)

#TODO: Confusion functionality in frontend
class Confusion(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Confusion", stacks, infinite)
  def tick(self, grid, creature):
      super().tick(grid, creature)

#TODO: Mindbreak functionality in frontend
class Mindbreak(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Mindbreak", stacks, infinite)
  def tick(self, grid, creature):
      super().tick(grid, creature)

class MidasCurse(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Midas Curse", stacks, infinite)
  def tick(self, grid, creature):
      total_gold = 0
      for item in creature.inventory:
          if item.name == "Gold":
              total_gold += item.amount
      creature.hp -= total_gold
      super().tick(grid, creature)

class Bloodsiphon(StatusEffect):
  def __init__(self, stacks, infinite, applicator):
      super().__init__("Bloodsiphon", stacks, infinite)
      self.applicator = applicator
  def tick(self, grid, creature):
      if self.applicator.hp <= 0:
          creature.status_effects.remove(self)
      creature.hp -= self.stacks
      if self.applicator.hp + self.applicator.stacks > self.applicator.max_hp:
          self.applicator.hp = self.applicator.max_hp
      else:
          self.applicator.hp += self.stacks

class Manadrain(StatusEffect):
  def __init__(self, stacks, infinite, applicator):
      super().__init__("Manadrain", stacks, infinite)
      self.applicator = applicator
  def tick(self, grid, creature):
      if self.applicator.hp <= 0:
          creature.status_effects.remove(self)
      creature.mp -= self.stacks
      if self.applicator.mp + self.applicator.stacks > self.applicator.max_mp:
          self.applicator.mp = self.applicator.max_mp
      else:
          self.applicator.mp += self.stacks


class Death(StatusEffect):
  def __init__(self, stacks, infinite, applicator):
      super().__init__("Death", stacks, infinite)
      self.applicator = applicator
  def tick(self, grid, creature):
      if self.applicator.hp <= 0:
          creature.status_effects.remove(self)
      if self.stacks <= 1:
          creature.die()
      super().tick(grid, creature)

#positive statuses

class Regeneration(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Regeneration", stacks, infinite)
  def tick(self, grid, creature):
      if creature.hp + self.stacks > creature.max_hp:
          creature.hp = creature.max_hp
      else:
          creature.hp += self.stacks
      super().tick(grid, creature)

#TODO: Blindness functionality in basic_attack_damage
class Berserk(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Berserk", stacks, infinite)
  def tick(self, grid, creature):
      super().tick(grid, creature)

class Flight(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Flight", stacks, infinite)
  def tick(self, grid, creature):
      super().tick(grid, creature)

#TODO: Luck functionality in item drop code
class Luck(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Luck", stacks, infinite)
  def tick(self, grid, creature):
      super().tick(grid, creature)

class Ironskin(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Ironskin", stacks, infinite)
  def on_apply(self, grid, creature):
      lightning_resistance_id = lookup_damage_type_id("LTG")
      for i in range(creature.damage_resistances):
          if i == lightning_resistance_id:
              creature.damage_resistances[i] -= 1.5
          else:
              creature.damage_resistances[i] += 0.1
  def tick(self, grid, creature):
      super().tick(grid, creature)
  def on_remove(self, grid, creature):
      lightning_resistance_id = lookup_damage_type_id("LTG")
      for i in range(creature.damage_resistances):
          if i == lightning_resistance_id:
              creature.damage_resistances[i] += 1.5
          else:
              creature.damage_resistances[i] -= 0.1

class Agility(StatusEffect):
  def __init__(self, stacks, infinite):
      super().__init__("Agility", stacks, infinite)
  def on_apply(self, grid, creature):
      creature.dodge += 2
  def tick(self, grid, creature):
      super().tick(grid, creature)
  def on_remove(self, grid, creature):
      creature.dodge -= 2