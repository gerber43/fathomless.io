from Level import Biome

class TempBiome(Biome):
    def __init__(self):
        super().__init__("Complex", "Wall", "Stair", [("Goblin", 1.0)], ["Door", "Pit"])