from GameObject import Item, Consumable, Equippable, Weapon, Unavailable, LightSourceItem
from SubSystem import lookup_damage_type_id

class IronDagger(Weapon):
    def __init__(self, pos, level):
        super().__init__("Iron Dagger", "17", pos, level, 5, ("Right Hand", "Left Hand"), "One-Handed Blade", 1, 3, [(lookup_damage_type_id("Piercing"), 3, 1)], [])
    def on_equip(self, grid, equipped_creature):
        pass
    def on_unequip(self, grid, equipped_creature):
        pass

class WoodenClub(Weapon):
    def __init__(self, pos, level):
        super().__init__("Wooden Club", "17", pos, level, 1, ("Right Hand", "Left Hand"), "One-Handed Mace", 1, 1.5, [(lookup_damage_type_id("Blunt"), 5, 0)], [])
    def on_equip(self, grid, equipped_creature):
        pass
    def on_unequip(self, grid, equipped_creature):
        pass
