from GameObject import Terrain

class Wall(Terrain):
    def __init__(self, pos):
        super().__init__("Wall", "#", pos, 200, (0.7, 0.9, 1, 1, 0.7, 1, 1, 0.5, 1, 1, 1, 1, 1), False, True, "NO", "")

class Pit(Terrain):
    def __init__(self, pos):
        super().__init__("Pit", "", pos, 1, (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), True, False, "WALK", "Are you sure you want to fall that far?")

    def onStep(self, creature):
        #if statement to check if creature is not flying, using status effect subsystem
            creature.hp -= 200*(1-creature.resistances.getResistance("BLT"))