from abc import abstractmethod

#damage type and resistance subsystem
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
