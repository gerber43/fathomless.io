from Level import Biome

class TempBiome(Biome):
    def __init__(self):
        super().__init__("Complex", "Wall", "Stairs", ["Goblin"], [10], ["Door", "Pit"], 22, [], None, -1)
        self.decor_spawns = {"StandingTorch": 0.05}

class Caves(Biome):
    def __init__(self):
        super().__init__("Cave", "Wall", "Stairs",
                         ["Goblin", "Bandit", "Ogre", "Spider", "Bat"],
                         [20, 10, 5, 10, 15],
                         ["Door", "Pit", "Rock", "Water", "LightBeam"],
                         [20, 2, 10, 2, 10],
                         4, [(1, "Cove", 1), (4, "Mine", 1), (4, "Sewer", 1)],
                         None, -1)
        self.floorTexture = "3"

class Cove(Biome):
    def __init__(self):
        super().__init__("Cave", "Wall", "Stairs",
                         ["Fishman", "FishmanShaman", "GiantCrab", "Pirate", "Drowned", "DrownedSailor", "DrownedPirate"],
                         [20, 5, 5, 10, 20, 15, 10],
                         ["Door", "Pit", "Water", "DeepWater", "Coral", "LightBeam"],
                         [20, 2, 40, 20, 10, 2],
                         2, [(2, "Cave", 4)],
                         "DrownedCaptain", 2)
        self.floorTexture = "4"                 

class Mine(Biome):
    def __init__(self):
        super().__init__("Cave&Complex", "Wall", "Stairs",
                         ["GoblinMiner", "HobgoblinMiner", "RockWorm", "Troll"],
                         [20, 10, 5, 5],
                         ["Door", "Pit", "Rock", "Deposit", "StandingTorch"],
                         [20, 2, 10, 1, 3],
                         4, [(1, "CorruptiteMine", 1), (4, "MagmaCore", 1), (4, "DeepCavern", 1)],
                         None, -1)
        self.floorTexture = "13"                 

#NOTE: both types of miners spawn with corruptite in their inventories when spawning here, and they will use it when they see the player
class CorruptiteMine(Biome):
    def __init__(self):
        super().__init__("Cave&Complex", "Wall", "Stair",
                         ["GoblinMinerAddict", "HobgoblinMinerAddict", "RockWorm", "Troll", "CorruptWorm", "CorruptTroll"],
                         [20, 10, 5, 5, 10, 10],
                         ["Door", "Pit", "Rock", "Deposit", "CorruptiteCluster", "StandingTorch"],
                         [20, 2, 10, 1, 1, 3],
                         2, [(2, "Mine", 4)],
                         "CorruptBehemoth", 2)
        self.floorTexture = "13"                 



class Sewer(Biome):
    def __init__(self):
        super().__init__("Labyrinth(Large)", "Wall", "Stair",
                         ["GiantSlime", "Frogman", "TrashLobster", "SewerCroc", "Gorefish", "Psyfish", "MasterThief"],
                         [20, 10, 5, 10, 5, 5, 1],
                         ["Door", "Pit", "Water", "DeepWater", "StandingTorch"],
                         [20, 2, 50, 30, 10],
                         4, [(1, "Shantytown", 1), (4, "DeepCavern", 1)],
                         None, -1)
        self.floorTexture = "5"                 


class Shantytown(Biome):
    def __init__(self):
        super().__init__("Complex", "Pit", "Stair",
                         ["DiseasedScavenger", "BloatedGuard", "Stinkfly"],
                         [20, 10, 10],
                         ["Door", "Wall", "StandingTorch"],
                         [20, 50, 10],
                         2, [(2, "Sewer", 4)],
                         "Rotmother", 2)
        self.floorTexture = "9"                 

class MagmaCore(Biome):
    def __init__(self):
        super().__init__("Cave", "Wall", "Stair",
                         ["FireSprite", "FireElemental", "MagmaGolem"],
                         [20, 10, 5],
                         ["Lava"],
                         [1],
                         3, [(3, "Embers", 1)],
                         None, -1)
        self.floorTexture = "15"                 

class DeepCavern(Biome):
    def __init__(self):
        super().__init__("Cave(Large)", "Wall", "Stair",
                         ["Bat", "DarkElf", "DarkDwarf", "Uln", "ElderUln", "CaveToad", "GiantSpider", "CaveGiant"],
                         [25, 20, 20, 10, 5, 10, 10, 1],
                         ["Water", "Rock"],
                         [1, 4],
                         3, [(1, "Ziggurat", 1), (3, "Undercity", 1)],
                         None, -1)
        self.floorTexture = "15"                 

class Ziggurat(Biome):
    def __init__(self):
        super().__init__("Complex", "Wall", "Portal",
                         ["XotilWarrior", "XotilAbomination", "XotilPriest", "DarkSerpent"],
                         [25, 10, 10, 5],
                         ["StoneDoor", "StandingTorch"],
                         [4, 1],
                         3, [(3, "Catacomb", 1), (3, "Carrion", 1)],
                         "Xotil High Priest", 3)
        self.floorTexture = "3"                 

class Embers(Biome):
    def __init__(self):
        super().__init__("Cave(Large)", "Wall", "Stair",
                         ["FireSprite", "AshGolem", "ObsidianGolem"],
                         [20, 10, 5],
                         ["Rock", "Ember", "Pit"],
                         [20, 5, 2],
                         1, [(1, "Columbarium", 1)],
                         "AshColossus", 1)
        self.floorTexture = "3"                 

class Undercity(Biome):
    def __init__(self):
        super().__init__("City", "Wall", "Stair",
                         ["DarkElf", "DarkElfSorceress", "Drider"],
                         [30, 10, 5],
                         ["StoneDoor", "Water", "Rock"],
                         [10, 5, 10],
                         1, [(1, "Catacomb", 1)],
                         "DarkElfQueen", 1)
        self.floorTexture = "3"                 


class Columbarium(Biome):
    def __init__(self):
        super().__init__("Complex", "Wall", "Stair",
                         ["AshGolem", "AshGhoul", "AshWight", "Ghost", "Wraith"],
                         [10, 10, 5, 5, 5],
                         ["StoneDoor", "Urn", "SpiritLight"],
                         [20, 10, 5],
                         1, [(1, "Catacomb", 2)],
                         None, -1)
        self.floorTexture = "3"                 

class Catacomb(Biome):
    def __init__(self):
        super().__init__("Labyrinth", "Wall", "Stair",
                         ["Zombie", "Skeleton", "Ghost", "Wraith", "Ghoul", "Ghast", "Wight", "Necromancer", "Vampire"],
                         [30, 25, 10, 5, 10, 5, 5, 1, 1],
                         ["StoneDoor", "Urn", "SpiritLight"],
                         [20, 10, 5],
                         3, [(3, "Necropolis", 1)],
                         None, -1)
        self.floorTexture = "3"                 

class Carrion(Biome):
    def __init__(self):
        super().__init__("Cave(Large)", "Wall", "Stair",
                         ["Blank", "Unfinished", "FleshAmalgam", "Polyp"],
                         [20, 10, 5, 5],
                         ["Blood", "LightGrowth"],
                         [20, 5],
                         2, [(2, "WorldeatersGut", 1)],
                         None, -1)
        self.floorTexture = "3"                 

class WorldeatersGut(Biome):
    def __init__(self):
        super().__init__("Intestinal", "Wall", "Stair",
                         ["Parasite", "BloodCrawler", "Devourer"],
                         [20, 10, 5],
                         ["Bile", "LightGrowth"],
                         [20, 5],
                         2, [(2, "AncientCity", 1)],
                         "WorldeaterHeart", 2)
        self.floorTexture = "3"                 

class Necropolis(Biome):
    def __init__(self):
        super().__init__("City", "Wall", "Stair",
                         ["Zombie", "Skeleton", "Ghost", "Wraith", "Ghoul", "Ghast", "Wight", "Lich", "DeathKnight", "WraithLord"],
                         [30, 25, 20, 20, 20, 20, 20, 5, 5, 5],
                         ["StoneDoor", "SpiritLight"],
                         [20, 5],
                         1, [(1, "Underworld1", 1)],
                         "DeadKing", 1)
        self.floorTexture = "3"                 

class Underworld1(Biome):
    def __init__(self):
        super().__init__("Cave", "Wall", "Stair",
                         ["Imp", "Demon", "Hellhound", "Hellbat", "TricksterImp", "ConfusedSoul", "DeceitDemon"],
                         [20, 10, 15, 20, 40, 35, 20],
                         ["Lava"],
                         [1],
                         1, [(1, "Underworld2", 1)],
                         "DecietArchdemon", 1)
        self.floorTexture = "3"                 

class Underworld2(Biome):
    def __init__(self):
        super().__init__("Cave", "Wall", "Stair",
                         ["Imp", "Demon", "Hellhound", "Hellbat", "AngryImp", "RageDemon"],
                         [20, 10, 15, 20, 40, 20],
                         ["Lava"],
                         [1],
                         1, [(1, "Underworld3", 1)],
                         "RageArchdemon", 1)
        self.floorTexture = "3"                 

class Underworld3(Biome):
    def __init__(self):
        super().__init__("Cave", "Wall", "Stair",
                         ["Imp", "Demon", "Hellhound", "Hellbat", "CovetousImp", "CharitableSoul", "GreedDemon"],
                         [20, 10, 15, 20, 40, 35, 20],
                         ["Lava"],
                         [1],
                         1, [(1, "Underworld4", 1)],
                         "GreedArchdemon", 1)
        self.floorTexture = "3"                 

class Underworld4(Biome):
    def __init__(self):
        super().__init__("Cave", "Wall", "Stair",
                         ["Imp", "Demon", "Hellhound", "Hellbat", "SadImp", "LostSoul", "DepressedDemon"],
                         [20, 10, 15, 20, 40, 35, 20],
                         ["Lava"],
                         [1],
                         1, [(1, "Underworld5", 1)],
                         "HopelessArchdemon", 1)
        self.floorTexture = "3"                 

class Underworld5(Biome):
    def __init__(self):
        super().__init__("Cave", "Wall", "Stair",
                         ["Imp", "Demon", "Hellhound", "Hellbat", "PeacefulSoul", "FateDemon", "FinalDemon"],
                         [20, 10, 15, 20, 40, 20, 20],
                         ["Lava"],
                         [1],
                         1, [(1, "WorldHeart", 1)],
                         "DoomArchdemon", 1)
        self.floorTexture = "3"                 

class AncientCity(Biome):
    def __init__(self):
        super().__init__("Complex", "MysticMist", "Stair",
                         ["AncientServant", "Apparition", "Memory"],
                         [20, 10, 5],
                         ["StoneDoor", "MysticMist"],
                         [20, 1],
                         2, [(2, "OldTemple", 1)],
                         None, -1)
        self.floorTexture = "3"                 

class OldTemple(Biome):
    def __init__(self):
        super().__init__("Complex(Large)", "Wall", "Portal",
                         ["Cultist", "Shambler", "WrithingOne", "DeepLord", "Mother", "Destroyer", "Scholar", "Schemer"],
                         [20, 10, 5, 1, 1, 1, 1, 1],
                         ["StoneDoor", "Spikes"],
                         [20, 5],
                         2, [(2, "CosmicVoid", 1)],
                         None, -1)
        self.floorTexture = "3"                 

class CosmicVoid(Biome):
    def __init__(self):
        super().__init__("Void", "AbsoluteNothingness", "Portal",
                         ["VoidBeast", "StarEater", "Annihilator"],
                         [20, 10, 5],
                         ["Energy"],
                         [1],
                         1, [(1, "WorldHeart", 1)],
                         "GreatDreamer", 1)
        self.floorTexture = "3"                 

class WorldHeart(Biome):
    def __init__(self):
        super().__init__("None", "Pit", "",
                         ["AbyssDragon"],
                         [1],
                         [],
                         [],
                         1, [],
                         "AbyssDragon", -1)
        self.floorTexture = "3"                 
