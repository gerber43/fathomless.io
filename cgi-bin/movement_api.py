#!/usr/bin/python3
import sys
import json
import cgi
import os
import pickle
from map_simplifier import delete_blank_object
from user_tracking import *
from GameObject import *
from Creatures import Goblin
from MasterGenerator import generateMap
from Terrain import *
from Decor import Corpse
from Races import *
import Enchantment
import cgitb
import copy
cgitb.enable()

print('Content-type: application/json\n')
HTTP_FIELDS = cgi.FieldStorage()
depth = 0
field_of_view = 11
fov_radius = field_of_view // 2 
turn_log = []
game_log = ""
gameOver = False

#Funciton to save the updated map
def save_map(map_file_path, map_data):
    with open(map_file_path, 'wb') as pickle_file:
        pickle.dump(map_data, pickle_file)
    
#Function to load the map file
def load_map(map_file_path):
    with open(map_file_path, 'rb') as pickle_file:
        return pickle.load(pickle_file)

# Function to find the player's current position on the map
def find_player_position(game_map):
    for x, row in enumerate(game_map):
        for y, tile in enumerate(row):
            for gameObject in (tile):
                if isinstance(gameObject, Player):
                    
                    return[x,y]
    return None  # If player is not found

#given a tile and a gameObject className (Creature, Terrain, ...) object is returned
def get_object_by_class(tile,className):
    parsedTile = [gameObject for gameObject in tile if gameObject.__class__.__base__.__name__ == className]
    return None if (len(parsedTile) == 0) else parsedTile[0]
    
# Function to process Creature's movement
def process_Creature_movement(position, direction, game_map):
    global turn_log 
    global game_log 
    x, y = position
    if direction == 0:  # Move right
        new_x, new_y = x + 1, y
    elif direction == 270:  # Move up
        new_x, new_y = x, y - 1
    elif direction == 180:  # Move left
        new_x, new_y = x - 1, y
    elif direction == 90:  # Move down
        new_x, new_y = x, y + 1
    else:
        return position, "Invalid direction"
    # Validate the new position
    creature = get_object_by_class(game_map[position[0]][position[1]],"Creature")
    if creature and len(creature.segments) > 0:
        for segment in creature.segments:

            if not is_valid_move(segment.pos[0] - x + new_x, segment.pos[1] - y + new_y, game_map, True):
                return position, "cannot fit"
    
    if not is_valid_move(new_x, new_y, game_map):
        
        if (len(game_map) > new_x and len(game_map) > new_y and get_object_by_class(game_map[new_x][new_y],"Terrain") and get_object_by_class(game_map[position[0]][position[1]],"Player")):
            terrain = get_object_by_class(game_map[new_x][new_y],"Terrain")
            attacker = get_object_by_class(game_map[position[0]][position[1]],"Player")
            damage = terrain.hp
            terrain.hp -= 20
            terrain.damaged = True
            damage = damage - terrain.hp
            
            turn_log.append({"type":"attack","before":get_relative_tile(attacker.pos),"after":get_relative_tile(terrain.pos),"amount":damage})
            game_log += attacker.name +" @ "+str(((attacker.pos)))+" Attacked "+terrain.name +" @ "+str((terrain.pos))+" For "+str(damage)+"\n"
            if terrain.hp <= 0:
                game_map[terrain.pos[0]][terrain.pos[1]].remove(terrain)
                game_log += attacker.name +" @ "+str(((attacker.pos)))+" Destroyed "+terrain.name +" @ "+str((terrain.pos))+"\n"

                return position, "terrain destoyed"
            return position, "terrain hit"
        return position, "You cannot move here"  # Invalid move
    
    # Update the Creature's position in the map
    
    message = "Creature has moved"
    creatureType = "Creature"
    if (get_object_by_class(game_map[x][y],creatureType) == None):
        creatureType = "Player"
        
    turn_log.append({"type":"movement","before":get_relative_tile(get_object_by_class(game_map[x][y],creatureType).pos),"after":get_relative_tile([new_x,new_y])})
    game_log += get_object_by_class(game_map[x][y],creatureType).name +" @ "+str(((get_object_by_class(game_map[x][y],creatureType).pos)))+" Moved To "+str(([new_x,new_y]))+"\n"
    
    get_object_by_class(game_map[x][y],creatureType).move(game_map,[new_x, new_y])
    if get_object_by_class(game_map[new_x][new_y],"Terrain"):
        get_object_by_class(game_map[new_x][new_y],"Terrain").on_step(game_map,get_object_by_class(game_map[new_x][new_y],creatureType))
    
    target = get_object_by_class(game_map[new_x][new_y],creatureType)
    for i in range(len(target.status_effects)):
        target.status_effects[i].tick(game_map,target)
    if (target.hp <= 0):
        if (isinstance(target,Player)):
            global gameOver
            gameOver = True
            return (new_x, new_y), message
        else:
            global player_pos
            #turn_log.append({"killed":"type"}) 
            game_log += target.name +" @ "+str(((target.pos)))+" Died In "+get_object_by_class(game_map[new_x][new_y],"Terrain").name+"\n"

            target.die(game_map,get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player"),Corpse(target.pos,target.hp,target.damage_resistances))
    return (new_x, new_y), message

# Function to update all Creature positions
def update_Creature_position(game_map, player_pos):
    player_pos = (list(player_pos))
    player = get_object_by_class(game_map[player_pos[0]][player_pos[1]], "Player")

    moved_Creatures = []  # Track Creatures that have already moved
    
    for x, row in enumerate(game_map):
        for y, tile in enumerate(row):
            
            Creature = get_object_by_class(game_map[x][y],"Creature")
            manhattan = abs(player_pos[0] - x) + abs(player_pos[1] - y)
            check = 10

            if Creature and not isinstance(Creature, Player) and Creature not in moved_Creatures:
                #if the creture is unable to detect the player, skip the tracking
                if not is_player_avalible(player_pos, player, Creature):
                    
                    direction = default_movement((x, y), game_map, Creature)
                    if direction is not None:
                        current_pos = (x, y)
                        current_pos, message = process_Creature_movement(current_pos, direction, game_map)
                    moved_Creatures.append(Creature)
                    continue  # Move to the next creature
                    
                # Get creature and player attack ranges safely
                
                creature_range = getattr(Creature.equipment[0], 'range', 1)
                player_range = getattr(player.equipment[0], 'range', 1)
                
                #if the creature's attack range is greater than player's, and the creature is in the player's attack range, it will move away from player
                if creature_range > player_range and manhattan <= player_range:
                    current_pos = (x,y)
                    for move_num in range(Creature.speed):
                        direction = find_escape_direction((x, y), player_pos, game_map, Creature)
                        if direction is not None:
                            current_pos, message = process_Creature_movement(current_pos, direction, game_map)
                        else:
                            break  # No valid direction to move away
                    moved_Creatures.append(Creature)
            
                #if player is in the creature's attack range, creature will attack player
                elif hasattr(Creature.equipment[0],"range") and manhattan <= int((Creature.equipment[0]).range):
                    process_attack(Creature, player)
                    moved_Creatures.append(Creature)
                
                #creature will move toward player if the player is in the tracking range
                elif manhattan <= check:
                    path_avoid_terrain = a_star((x, y), player_pos, game_map, Creature, False)
                    path_destruct_terrain = a_star((x, y), player_pos, game_map, Creature, True)
                    cost_avoid = len(path_avoid_terrain) - 1 if path_avoid_terrain else float('inf')
                    cost_destruct = calculate_destruct_path_cost(path_destruct_terrain, Creature, game_map) if path_destruct_terrain else float('inf')
                    turn_needed = 0 

                    if cost_destruct < cost_avoid:
                        path = path_destruct_terrain
                    else:
                        path = path_avoid_terrain
                    
                    if not path or len(path) < 2:
                        continue
                        
                    current_pos = (x, y)
                    path_index = 1  # Start from the next position in the path
                    moves_remaining = Creature.speed

                    while moves_remaining > 0 and path_index < len(path):
                        next_pos = path[path_index]
                        next_terrain = get_object_by_class(game_map[next_pos[0]][next_pos[1]], "Terrain")
                        if next_terrain and not next_terrain.passable:
                            process_attack_to_terrain(Creature, next_terrain)
                            moves_remaining -= 1    # Spent a turn attacking
                        else:
                            direction = get_direction_from_step(current_pos, next_pos)
                            if direction is not None:
                                current_pos, message = process_Creature_movement(current_pos, direction, game_map)
                                current_pos = next_pos  # Update current position
                                path_index += 1
                                moves_remaining -= 1
                    moved_Creatures.append(Creature)
                    
                  
                # Perform default movement if no other action is taken
                else:
                    direction = default_movement((x, y), game_map, Creature)
                    if direction is not None:
                        current_pos = (x, y)
                        current_pos, message = process_Creature_movement(current_pos, direction, game_map)
                    moved_Creatures.append(Creature)

#helper funtion to caculate the the turn needed for path of destroying terrain
def calculate_destruct_path_cost(path, creature, game_map):
    total_cost = 0
    for i in range(len(path) - 1):
        next_pos = path[i + 1]
        terrain = get_object_by_class(game_map[next_pos[0]][next_pos[1]], "Terrain")
    if terrain and not terrain.passable and not is_destructible(terrain_copy, game_map):
        return float('inf')
    if terrain and not terrain.passable and is_destructible(terrain_copy, game_map):
            terrain_copy = copy.deepcopy(terrain)
            while (terrain_copy.hp > 0):
                #creature.bassic_attack(game_map, terrain_copy)
                terrain_copy.hp -= 20
                total_cost += 1
                
            
    total_cost += len(path) - 1
    return total_cost
                    
#helper funtion to check if the creature can detect the player
def is_player_avalible(player_pos, Player, Creature):
    Light = None
    for objects in game_map[player_pos[0]][player_pos[1]]:
        if objects.name == "Light":
            Light = objects
            break
    #if the Player's current position have 0 light intensity, The creature can't detect The player
    
    if Light:
        if Light.intensity == 0:
            return False

        #if the Player's stealth skills is greater than the Creature's perception * Light lvel, Creature can't detect The player
        
        if Creature.perception * Light.intensity < Player.skills[19]:
            return False

    #otherwise, creature can detect the player
    return True

    
# Helper function to get direction between two points
def get_direction_from_step(current_pos, next_pos):
    if next_pos:
        dx = next_pos[0] - current_pos[0]
        dy = next_pos[1] - current_pos[1]
    
        if dx == 1 and dy == 0:
            return 0  # Right
        elif dx == -1 and dy == 0:
            return 180  # Left
        elif dx == 0 and dy == 1:
            return 90  # Down
        elif dx == 0 and dy == -1:
            return 270  # Up
    return None  # No valid direction
    

# Function to validate the movement
def is_valid_move(x, y, game_map, isMultiTile = False):
    if x < 0 or y < 0 or x >= len(game_map) or y >= len(game_map[0]): #out of bounds
        return False
    if get_object_by_class(game_map[x][y],"Creature") and not isMultiTile:
        return False
    if get_object_by_class(game_map[x][y],"CreatureSegment") and not isMultiTile:
        return False
    if get_object_by_class(game_map[x][y],"Player"):
        return False
    if (get_object_by_class(game_map[x][y],"Terrain") and not get_object_by_class(game_map[x][y],"Terrain").passable and (get_object_by_class(game_map[x][y],"Decor") and get_object_by_class(game_map[x][y],"Decor").passable)):
        return True #if non passable terrain but passable decor 
    if (get_object_by_class(game_map[x][y],"Terrain") and not get_object_by_class(game_map[x][y],"Terrain").passable):
        return False
    if ((get_object_by_class(game_map[x][y],"Decor") and not get_object_by_class(game_map[x][y],"Decor").passable)):
        return False
    
    return True
#Function to create the subset of map
def get_map_subset(player_pos, game_map, fov_radius):
    x, y = player_pos
    x_max = len(game_map)
    y_max = 0;
    if x_max > 0:
        y_max = len(game_map[0])

    blank_tile = {"Bottom": {"textureIndex": 8}}
    
    map_subset = []
    for i in range(x - fov_radius, x + fov_radius + 1):
        row_subset = []
        for j in range(y- fov_radius, y + fov_radius + 1):
            if i < 0 or i >= x_max or j < 0  or j >= y_max:
                row_subset.append(blank_tile)
            else:
                bottomTexture = 0
                segment = None
                for objects in game_map[i][j]:
                    if objects.name == "Segment":
                        segment = {"textureIndex":objects.creature.textureIndex,'hp':objects.creature.hp,'creature':objects.creature.pos}
                        game_map[i][j].remove(objects)
                        break
                for objects in game_map[i][j]:
                    if objects.name == "Bottom":
                        bottomTexture = objects.textureIndex
                        del objects
                        break;
                internalGrid = {gameObject.__class__.__base__.__name__.capitalize(): gameObject.__dict__ for gameObject in game_map[i][j]}
                if (internalGrid.get('Gameobject') is not None):
                    internalGrid['Light'] = internalGrid['Gameobject']
                    del internalGrid['Gameobject']
                    internalGrid['Bottom'] = {"textureIndex":bottomTexture}

                if segment:
                   
                    internalGrid['Creature'] = segment

                if (internalGrid.get('Shop') is not None):
                    internalGrid['Decor'] = internalGrid['Shop']
                    for inventory in range(len(internalGrid['Decor']['inventory'])):
                        if isinstance(internalGrid['Decor']['inventory'][inventory],GameObject):
                            internalGrid['Decor']['inventory'][inventory] = internalGrid['Decor']['inventory'][inventory].__dict__
                    del internalGrid['Shop']
                    
                
                if (internalGrid.get('Weapon') is not None):
                    internalGrid['Item'] = internalGrid['Weapon']
                    del internalGrid['Weapon']
                    
                if (internalGrid.get('Consumable') is not None):
                    internalGrid['Item'] = internalGrid['Consumable']
                    del internalGrid['Consumable']
                    
                if (internalGrid.get('Equippable') is not None):
                    internalGrid['Item'] = internalGrid['Equippable']
                    del internalGrid['Equippable']
                    
                if (internalGrid.get('Lightterrain') is not None):
                    internalGrid['Terrain'] = internalGrid['Lightterrain']
                    del internalGrid['Lightterrain']
                if (internalGrid.get('Lightdecor') is not None):
                    internalGrid['Decor'] = internalGrid['Lightdecor']
                    del internalGrid['Lightdecor']
                if (internalGrid.get('Lightsourceitem') is not None):
                    internalGrid['Item'] = internalGrid['Lightsourceitem']
                    del internalGrid['Lightsourceitem']
                if (internalGrid.get('Player') is not None):
                    internalGrid['Creature'] = internalGrid['Player']
                    del internalGrid['Player']
                if (internalGrid.get('Weapon') is not None):
                    #internalGrid['Weapon']['enchantment'] = internalGrid['Weapon']['enchantment'].name;
                    internalGrid['Item'] = internalGrid['Weapon']
                if (internalGrid.get('Consumable') is not None):
                    #internalGrid['Weapon']['enchantment'] = internalGrid['Weapon']['enchantment'].name;
                    internalGrid['Item'] = internalGrid['Consumable']
                if (internalGrid.get('Equippable') is not None):
                    #internalGrid['Weapon']['enchantment'] = internalGrid['Weapon']['enchantment'].name;
                    internalGrid['Item'] = internalGrid['Equippable']
                    

                
                if (internalGrid.get('Creature') is not None and not segment):
                    
                    
                    if (internalGrid['Creature'].get('turns')):
                        internalGrid['Creature']['score'] = internalGrid['Creature']['score'] - internalGrid['Creature']['turns']
                    
                    
                    
                    
                    del internalGrid['Creature']['segments']
                    #for segment in range(len(internalGrid['Creature']['segments'])):
                        #internalGrid['Creature']['segments'] = "Segments Present"
                        #internalGrid['Creature']['segments'][segment].creature = internalGrid['Creature']['segments'][segment].creature.pos
                        #internalGrid['Creature']['segments'][segment] = internalGrid['Creature']['segments'][segment].__dict__

                    for a in range(len(internalGrid['Creature']['equipment'])):
                        if hasattr(internalGrid['Creature']['equipment'][a], 'statuses'):
                            for b in range(len(internalGrid['Creature']['equipment'][a].statuses)):
                                internalGrid['Creature']['equipment'][a].statuses[b] = internalGrid['Creature']['equipment'][a].statuses[b].__dict__
                    
                    internalGrid['Creature']['status_effects'] = [status_effects.__dict__ for status_effects in internalGrid['Creature']['status_effects'] if status_effects]
                    internalGrid['Creature']['equipment'] = [equipment.__dict__ for equipment in internalGrid['Creature']['equipment'] if equipment]
                    
                    internalGrid['Creature']['abilities'] = [abilities.__dict__ for abilities in internalGrid['Creature']['abilities'] if abilities]
                    
                        
                    '''
                    for i in range(len(internalGrid['Creature']['inventory'])):
                        if hasattr(internalGrid['Creature']['inventory'][i], 'enchantment'):
                            internalGrid['Creature']['inventory'][i].enchantment = internalGrid['Creature']['inventory'][i].enchantment.name
                   '''
                    internalGrid['Creature']['inventory'] = [inventory.__dict__ for inventory in internalGrid['Creature']['inventory'] if inventory]
                   
                    if (internalGrid['Creature'].get('drop_table') is not None):
                        del internalGrid['Creature']['drop_table']
                
                row_subset.append(internalGrid)
        map_subset.append(row_subset)
    
        
    
    return map_subset
    
    
#Function to get the target creature
def get_target_tile(tile):
    global player_pos
    global fov_radius
    global game_map
    player_x, player_y = player_pos
    fov_x_start = player_x - fov_radius
    fov_y_start = player_y - fov_radius
    target_x = fov_x_start + tile[0]
    target_y = fov_y_start + tile[1]
    
    if target_x < 0 or target_x >= len(game_map) or target_y < 0 or target_y >= len(game_map[0]):
        return None
    return [target_x,target_y]

def get_relative_tile(tile):
    global player_pos
    global fov_radius
    global game_map
    player_x, player_y = player_pos
    fov_x_start = player_x - fov_radius
    fov_y_start = player_y - fov_radius
    target_x = tile[0] - fov_x_start
    target_y = tile[1] - fov_y_start 
    
    if target_x < 0 or target_x >= len(game_map) or target_y < 0 or target_y >= len(game_map[0]):
        return None
    return [target_x,target_y]

#function to process the attack action to a terrain
def process_attack_to_terrain(attacker, terrain):
    
    global game_map
    beforeHp = terrain.hp
    #attacker.basic_attack(game_map, terrain)
    terrain.hp -= 20 
    terrain.damaged = True
    #temp terrain interaction
    
    
    damage = beforeHp - terrain.hp
    # reduce terrain's hp
    if (damage > 0):
        global turn_log 
        global game_log 
        turn_log.append({"type":"attack","before":get_relative_tile(attacker.pos),"after":get_relative_tile(terrain.pos),"amount":damage})
        game_log += attacker.name +" @ "+str(((attacker.pos)))+" Attacked "+terrain.name +" @ "+str((terrain.pos))+" For "+str(damage)+"\n"
    
        #check did the creature dead
        if terrain.hp <= 0:
            game_map[terrain.pos[0]][terrain.pos[1]].remove(terrain)
            return "terrain destoyed"
        return "terrain hit"
    else:
        return "terrain missed"
    

#funtion to process the acttack action to a creature
def process_attack(attacker, target):
    if isinstance(target,CreatureSegment):
        target = target.creature
    
    global game_map
    beforeHp = target.hp
    attacker.basic_attack(game_map, target)
    damage = beforeHp - target.hp
    # reduce target's hp
    if (damage > 0):
        global turn_log 
        global game_log 
        turn_log.append({"type":"attack","before":get_relative_tile(attacker.pos),"after":get_relative_tile(target.pos),"amount":damage})
        game_log += attacker.name +" @ "+str(((attacker.pos)))+" Attacked "+target.name +" @ "+str((target.pos))+" For "+str(damage)+"\n"
    
        #check did the creature dead
        if target.hp <= 0:
            target.die(game_map,get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player"),Corpse(target.pos,target.hp,target.damage_resistances))
            if isinstance(target,Player):
                global gameOver
                gameOver = True
            else:
                return "target killed"
                
        return "target hit"
    else:
        return "target missed"

def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False    
        
def find_current_level(game_map):
    for x, row in enumerate(game_map):
        for y, tile in enumerate(row):
            for gameObject in (tile):
                if gameObject.name == "Stairs":
                    return gameObject.hp
    return None  # If player is not found
def jsonify(array):
    if (isinstance(array,GameObject)):
        print(dir(array))
biomes_dict = {
    0: 'Caves: Opening',
    1: 'Caves: Middle Ground',            
    2: 'Caves: Deepest Layer',            
    3: 'Cove',             
    4: 'Mine',            
    5: 'Corruptite Mine',  
    6: 'Sewer: Access A',            
    7: 'Sewer Access B',            
    8: 'Shanty Town',       
    9: 'Magma Core',       
    10: 'Deep Cavern',     
    11: 'Ziggurat',        
    12: 'Embers',          
    13: 'Columbarium',     
    14: 'Catacomb',        
    15: 'Carrion',         
    16: 'Worldeaters Gut', 
    17: 'Necropolis',      
    18: 'Underworld',     
    19: 'Ancient City',    
    20: 'Old Temple',      
    21: 'Cosmic Void',     
    22: 'World Heart',
    23: 'World Heart'  
}
    
if (HTTP_FIELDS.getvalue('uuid')):
      uuid = HTTP_FIELDS.getvalue('uuid')
      direction = None
      attack = [int(coordinate) for coordinate in HTTP_FIELDS.getvalue('attack').split(",")] if HTTP_FIELDS.getvalue('attack') else None
      difficulty = HTTP_FIELDS.getvalue('difficulty') if (HTTP_FIELDS.getvalue('difficulty')) else "Easy"
      race = HTTP_FIELDS.getvalue('race') if (HTTP_FIELDS.getvalue('race')) else None
      name = HTTP_FIELDS.getvalue('name') if (HTTP_FIELDS.getvalue('name')) else "Name"
      interact = HTTP_FIELDS.getvalue('interact') if (HTTP_FIELDS.getvalue('interact')) else None
      buy = (HTTP_FIELDS.getvalue('buy')) if (HTTP_FIELDS.getvalue('buy')) else None
      sell = (HTTP_FIELDS.getvalue('sell')) if (HTTP_FIELDS.getvalue('sell')) else None
      skills = (HTTP_FIELDS.getvalue('skills')) if (HTTP_FIELDS.getvalue('skills')) else None
      levelUp = HTTP_FIELDS.getvalue('levelUp') if (HTTP_FIELDS.getvalue('levelUp')) else None
      fitness = int(HTTP_FIELDS.getvalue('fitness')) if (HTTP_FIELDS.getvalue('fitness')) else 0
      magic = int(HTTP_FIELDS.getvalue('magic')) if (HTTP_FIELDS.getvalue('magic')) else 0
      cunning = int(HTTP_FIELDS.getvalue('cunning')) if (HTTP_FIELDS.getvalue('cunning')) else 0
      field_of_view = int(HTTP_FIELDS.getvalue('fov')) if (HTTP_FIELDS.getvalue('fov')) else 11
      if field_of_view%2 == 0 or field_of_view <= 1 and field_of_view > 11:
          field_of_view = 11
      fov_radius = field_of_view // 2 

      


      selected = HTTP_FIELDS.getvalue('selected') if (HTTP_FIELDS.getvalue('selected')) else False
      level = HTTP_FIELDS.getvalue('level') if (HTTP_FIELDS.getvalue('level') and uuid == "Test") else "0"
      if (uuid == "Test"):
          difficulty = "Test"
    # Load the current map
      file_path = '../maps/'+uuid+'.pkl' 
      if (not os.path.exists(file_path)):
          player = eval(race)(-1, -1)
          player.name = name
          game_map = generateMap(0, level+","+difficulty,player)
          turn_log.append({"level":level+","+difficulty})
          game_log += "New Level Generated "+level+","+difficulty+"\n"
          message = "Welcome To The Caverns"
          
          if (int(level) == 23):
              gameOver = True
      else:
          game_map = load_map(file_path)
      
    # Process player's movement
      message = None
      player_pos = find_player_position(game_map)
     
      if (attack != None):
          target_coordinates = get_target_tile(attack)
          player = get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player")
          direction = get_direction_from_step(player_pos, target_coordinates)
          if (direction == 270):
             player.textureIndex = 36
          elif (direction == 0):
             player.textureIndex = 37
          elif (direction == 90):
             player.textureIndex = 38
          elif (direction == 180):
             player.textureIndex = 39
          target_creature = get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Creature")
          for objects in game_map[target_coordinates[0]][target_coordinates[1]]:
              if isinstance(objects,CreatureSegment):
                  target_creature = objects
          
          if (not interact and not selected and target_coordinates and target_creature): #attack when the target is a creature but not player
              
              message = process_attack(get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player"), target_creature)
              update_Creature_position(game_map, player_pos)
              
              player.turns += 1
          elif (not interact and not selected and target_coordinates and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Creature") == None and target_creature == None): #move
             
              if (abs(player_pos[0] - target_coordinates[0]) + abs(player_pos[1] - target_coordinates[1]) == 1):
                  
                  
                  player_pos, message = process_Creature_movement(player_pos, direction, game_map)
                  
                  
                  if (get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Item")):
                      get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").pickup_item(game_map,get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Item"))
                  if (get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Weapon")):
                      get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").pickup_item(game_map,get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Weapon"))
                  if (get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Consumable")):
                      get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").pickup_item(game_map,get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Consumable"))
                  if (get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Equippable")):
                      get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").pickup_item(game_map,get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Equippable"))
                  player.turns += 1
              else:
                  message = "Movement Out Of Range"
          
          
          if (target_coordinates and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Shop")):
              message = get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Shop").dialogue
              turn_log.append({"shop":"interacted"})
          
          
          if (target_coordinates and not target_creature and ((interact and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Decor")) or (message != "Creature has moved" and not selected and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Decor") and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Decor").name != "Stairs" and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Decor").name != "Corpse"))): #interact 
             
              get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Decor").on_interact(game_map,get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player"))
              
              message = "Creature has moved" if (message == "Creature has moved") else "interacted with"
              game_log += get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").name +" @ "+str(((get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").pos)))+" Interacted With "+get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Decor").name +" @ "+str(((get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Decor").pos)))+"\n"
              player.turns += 1
         
         
         
          if (selected):
              
              selected_method = selected.split(":")[0]
              selected_index = int(selected.split(":")[1])
              creatureType = "Creature"
              if (get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType) == None):
                  creatureType = "Player"
                  
              if (selected_method.lower() == "equipment" and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]], "Player")):
                  targetItem = get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").equipment[selected_index]
                  targetItem.on_unequip(game_map,get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player"))
                  game_log += targetItem.name+" Unequiped By "+get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).name+" @ "+str(get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).pos)
                  message = targetItem.name+" Unequiped By "+get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).name+" @ "+str(get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).pos)
                    
              if (selected_method.lower() == "inventory" and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]], creatureType)):
                  targetItem = get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").inventory[selected_index]
                    
                  if (targetItem.__class__.__base__.__name__ == "Consumable"):
                      get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").inventory[selected_index].use_effect(game_map,get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType))
                      get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").inventory[selected_index].amount -= 1
                      if (get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").inventory[selected_index].amount < 0):
                          get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").inventory.remove(get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").inventory[selected_index])
                      game_log += targetItem.name+" Consumed By "+get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).name+" @ "+str(get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).pos)
                      message = targetItem.name+" Consumed By "+get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).name+" @ "+str(get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).pos)
                      
                  if ((targetItem.__class__.__base__.__name__ == "Equippable") or (targetItem.__class__.__base__.__name__ == "Weapon")):
                      
                      get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").inventory[selected_index].on_equip(game_map,get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType))
                      game_log += targetItem.name+" Equipped Tp "+get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).name+" @ "+str(get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).pos)
                      message = targetItem.name+" Equipped To "+get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).name+" @ "+str(get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).pos)
                      
              if (selected_method.lower() == "abilities" and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType)):
                  get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").abilities[selected_index].use(game_map,get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player"),get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType))
                  targetAbility = get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").abilities[selected_index]
                  game_log += targetAbility.name+" Used On "+get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).name+" @ "+str(get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).pos)
                  message = targetAbility.name+" Used On "+get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).name+" @ "+str(get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],creatureType).pos)
                  
                  turn_log.append({"type":"ability","before":get_relative_tile(get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player").pos),"after":get_relative_tile(target_coordinates)})

      else:
          turn_log.append({"level":find_current_level(game_map)})
          message = "Welcome To The "+biomes_dict[int(find_current_level(game_map).split(",")[0])]

    #update the Creature's position
      if (message == "Creature has moved"):
          player_pos = find_player_position(game_map)

          update_Creature_position(game_map, player_pos)
          #print(get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Decor").name)
          if (get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Decor") and get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Decor").name == "Stairs") or (get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Terrain") and get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Terrain").name == "Pit"):
              if get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Decor") and get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Decor").name == "Stairs":
                  stair = get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Decor")
                  depth = str(int(stair.hp.split(",")[0]) + 1)+","+stair.hp.split(",")[1]
                  if ((int(stair.hp.split(",")[0]) + 1) == 23):
                      gameOver = True
              else:
                  depth = str(int(find_current_level(game_map).split(",")[0])+1)+","+find_current_level(game_map).split(",")[1]
              player = get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player")
              player.textureIndex = 38
              
              game_map = generateMap(0, depth,player)
              turn_log.append({"level":depth})
              message = "Welcome To The "+biomes_dict[int(depth.split(",")[0])]
              player_pos = find_player_position(game_map)
              game_log += "New Level Generated "+depth+"\n"
      player = get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Player")
      
      if buy != None:
          shop = get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Shop")
          if shop:
              if shop.buy(game_map, player, shop.inventory[int(buy)]):
                  turn_log.append({"buy":"bought:"+buy})
                  turn_log.append({"shop":"interacted"})
                  message = "Item Bought"
              else:
                  turn_log.append({"buy":"failed:"+buy})
                  turn_log.append({"shop":"interacted"})
                  message = "Thank You"
      if sell != None:
          shop = get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Shop")
          if shop:
              if shop.sell(game_map, player, player.inventory[int(sell)]):
                  turn_log.append({"sell":"sold:"+sell})
                  turn_log.append({"shop":"interacted"})
                  message = "Item Sold"
              else:
                  turn_log.append({"sell":"failed:"+sell})
                  turn_log.append({"shop":"interacted"})
                  message = "Sell Failed"
      turn_log.append({"race":player.race})

      points = 5 if player.__class__.__name__ != "Human" else 6
      totalSkills = 0
      if skills:
          skills = skills.split(",")
          for i in range(len(skills)):
              skills[i] = int(skills[i])
              totalSkills += skills[i]
      if (levelUp != None and player.xp >= 20*player.level and (fitness + cunning + magic) == 1 and totalSkills == points):
          player.fitness += fitness
          player.cunning += cunning
          player.magic += magic
          player.check_level(game_map)

          
          
          for i in range(len(skills)):
              player.skills[i] += skills[i]
          
          
          turn_log.append({"level_up":player.level})
          message = "Leveled Up To Level "+str(player.level)
          game_log += "Leveled Up To Level "+str(player.level)+"\n"
      if (levelUp != None and player.xp >= 20*player.level and (fitness + cunning + magic) != 1 and totalSkills == points):   
          turn_log.append({"level_up_menu":{"level":player.level + 1,"points":points}})
          message = "Please increase Fitness, Cunning or Magic"
      if (levelUp != None and player.xp >= 20*player.level and (fitness + cunning + magic) == 1 and totalSkills != points):   
          turn_log.append({"level_up_menu":{"level":player.level + 1,"points":points}})
          message = "Please spend "+str(points - totalSkills)+" more points"
      if (levelUp != None and player.xp >= 20*player.level and (fitness + cunning + magic) != 1 and totalSkills != points):   
          turn_log.append({"level_up_menu":{"level":player.level + 1,"points":points}})
          message = "Please spend "+str(points - totalSkills)+" more points and choose Fitness, Cunning or Magic"



      if player.xp >= 20*player.level:
          points = 5 if player.__class__.__name__ != "Human" else 6
          turn_log.append({"level_up_menu":{"level":player.level + 1,"points":points}})


    # Save the updated map back to the file
      save_map(file_path, game_map)
      
          
    # Caete the subset of the map
      
      map_subset = get_map_subset(player_pos, game_map, fov_radius)

    #send subset_map and message back to client
      
      if (gameOver):
         game_log += "Game Over. Final Score: "+str(player.score - player.turns)
      
      with open("../logs/"+uuid+".txt", "a") as myfile:
         myfile.write(game_log)
         
      if (gameOver):
         import urllib.request
         import urllib.parse
         full_game_log = urllib.request.urlopen('https://fathomless.io/gameOver/?uuid='+urllib.parse.quote_plus(uuid))
         turn_log.append({"type":"game_over","game_log":(full_game_log.read().decode("utf-8"))}) #end the game if the turn_log contain game_over
      for i in range(len(map_subset)):
          for j in range(len(map_subset[i])):
              objectKeys = list(map_subset[i][j].keys())
              for k in range(len(objectKeys)):
                  if not is_jsonable(map_subset[i][j][objectKeys[k]]):
                      print("here")
                      jsonify(map_subset[i][j][objectKeys[k]])
                      
                      map_subset[i][j][objectKeys[k]]['creature'] = "BAD"
      response = {
          "message": message if message else "",
          "map_subset": map_subset,
          "turn_log": turn_log
      }
      
      
      
      
      sys.stdout.write(json.dumps(response))
      
