from GameObject import *
from Terrain import *  
from Decor import *
from Creatures import *
from Items import *

def generateMap(width, height, depth, num_creatures, player, num_items):
    gameMap = [[[Bottom("Bottom", 1,(-1,-1)),Light((-1,-1),.8)] for _ in range(11)] for _ in range(11)]
    player.pos = [5, 5]
    gameMap[player.pos[0]][player.pos[1]].append(player)
    
    for x in range(len(gameMap)):
        for y in range(len(gameMap[x])):
            if ((((x - 5)**2) + (y - 5)**2) <= 6**2):
                for z in range(len(gameMap[x][y])):
                    if (gameMap[x][y][z].name == "Bottom"):
                        gameMap[x][y][z].textureIndex = "5"
            if ((((x - 5)**2) + (y - 5)**2) <= 2**2):
                for z in range(len(gameMap[x][y])):
                    if (gameMap[x][y][z].name == "Bottom"):
                        gameMap[x][y][z].textureIndex = "3"
                        
              
    weapons = LevelZeroWeaponShop([2,2])  
    gameMap[weapons.pos[0]][weapons.pos[1]].append(weapons)
    armor = LevelZeroArmorShop([8,2])
    gameMap[armor.pos[0]][armor.pos[1]].append(armor)
    scroll = LevelZeroScrollShop([5,9])
    gameMap[scroll.pos[0]][scroll.pos[1]].append(scroll)
    
    stairs = Stairs([1,5])
    stairs.hp = "0,easy"
    gameMap[stairs.pos[0]][stairs.pos[1]].append(stairs)
    
    stairs = Stairs([5,1])
    stairs.hp = "0,medium"
    gameMap[stairs.pos[0]][stairs.pos[1]].append(stairs)
    
    stairs = Stairs([9,5])
    stairs.hp = "0,hard"
    gameMap[stairs.pos[0]][stairs.pos[1]].append(stairs)
    
    
    
    
    return gameMap
