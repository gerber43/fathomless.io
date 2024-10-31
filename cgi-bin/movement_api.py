#!/usr/bin/python3
import sys
import json
import cgi
import os
import pickle
from map_simplifier import delete_blank_object
from user_tracking import a_star, find_escape_direction
from GameObject import *
from Creatures import Goblin, Player
from MasterGenerator import generateMap
from Terrain import Wall, Pit, Water, Fire, Spikes, EmptySpace
from Decor import Corpse
import cgitb
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
    if not is_valid_move(new_x, new_y, game_map):
        return position, "You cannot move here"  # Invalid move
    
    # Update the Creature's position in the map
    
    message = "Creature has moved"
    global turn_log
    global game_log
    turn_log.append({"type":"movement","before":get_relative_tile(get_object_by_class(game_map[x][y],"Creature").pos),"after":get_relative_tile([new_x,new_y])})
    game_log += get_object_by_class(game_map[x][y],"Creature").name +" @ "+str(((get_object_by_class(game_map[x][y],"Creature").pos)))+" Moved To "+str(([new_x,new_y]))+"\n"
    
    get_object_by_class(game_map[x][y],"Creature").move(game_map,[new_x, new_y])
    get_object_by_class(game_map[new_x][new_y],"Terrain").on_step(game_map,get_object_by_class(game_map[new_x][new_y],"Creature"))
    
    target = get_object_by_class(game_map[new_x][new_y],"Creature")
    if (target.hp <= 0):
        if (target.name == "Player"):
            global gameOver
            gameOver = True
            return (new_x, new_y), message
        else:
            global player_pos
            #turn_log.append({"killed":"type"}) 
            game_log += target.name +" @ "+str(((target.pos)))+" Died In "+get_object_by_class(game_map[new_x][new_y],"Terrain").name+"\n"

            target.die(game_map,get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Creature"),Corpse(target.pos,target.hp,target.damage_resistances))
    return (new_x, new_y), message

# Function to update all Creature positions
def update_Creature_position(game_map, player_pos):
    player_pos = (list(player_pos))
    Player = get_object_by_class(game_map[player_pos[0]][player_pos[1]], "Creature")

    moved_Creatures = []  # Track Creatures that have already moved
    
    for x, row in enumerate(game_map):
        for y, tile in enumerate(row):
            
            Creature = get_object_by_class(game_map[x][y],"Creature")
            manhattan = abs(player_pos[0] - x) + abs(player_pos[1] - y)
            check = 10

            if Creature and Creature.name != "Player" and Creature not in moved_Creatures:
                #if the creature's attack range is greater than player's, and the creature is in the player's attack range, it will move away from player
                if int((Creature.equipment[0]).range) > int((Player.equipment[0]).range) and manhattan <= int((Player.equipment[0]).range):
                    current_pos = (x,y)
                    for move_num in range(Creature.speed):
                        direction = find_escape_direction((x, y), player_pos, game_map)
                        current_pos, message = process_Creature_movement(current_pos, direction, game_map)
                    moved_Creatures.append(Creature)
            
                #if player is in the creature's attack range, creature will attack player
                elif manhattan <= int((Creature.equipment[0]).range):
                    process_attack(Creature, Player)
                    moved_Creatures.append(Creature)
                
                #creature will move toward player if the player is in the tracking range
                elif manhattan <= check:
                    path = a_star((x, y), player_pos, game_map)
                    if not path or len(path) < 2:
                        continue
                    current_pos = (x, y)
                    for move_num in range(min(Creature.speed, len(path) - 1)):
                        next_pos = path[move_num + 1]
                        direction = get_direction_from_step(current_pos, next_pos)  # Get direction for the move
                        current_pos, message = process_Creature_movement(current_pos, direction, game_map)
                    moved_Creatures.append(Creature)

# Helper function to get direction between two points
def get_direction_from_step(current_pos, next_pos):
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
    else:
        return None  # No valid direction

# Function to validate the movement
def is_valid_move(x, y, game_map):
    if x < 0 or y < 0 or x >= len(game_map) or y >= len(game_map[0]) or get_object_by_class(game_map[x][y],"Creature") or not get_object_by_class(game_map[x][y],"Terrain").passable:
        if ((get_object_by_class(game_map[x][y],"Decor") != None and get_object_by_class(game_map[x][y],"Decor").passable)):
            return True
        else:
            return False
    return True
#Function to create the subset of map
def get_map_subset(player_pos, game_map, fov_radius):
    x, y = player_pos
    x_max = len(game_map)
    y_max = 0;
    if x_max > 0:
        y_max = len(game_map[0])

    blank_tile = {"Terrain": {"textureIndex": 8}}
    
    map_subset = []
    for i in range(x - fov_radius, x + fov_radius + 1):
        row_subset = []
        for j in range(y- fov_radius, y + fov_radius + 1):
            if i < 0 or i >= x_max or j < 0  or j >= y_max:
                row_subset.append(blank_tile)
            else:
                internalGrid = {gameObject.__class__.__base__.__name__.capitalize(): gameObject.__dict__ for gameObject in game_map[i][j]}
                if (internalGrid.get('Creature') is not None):
                    internalGrid['Creature']['status_effects'] = [status_effects.__dict__ for status_effects in internalGrid['Creature']['status_effects'] if status_effects]
                    internalGrid['Creature']['equipment'] = [equipment.__dict__ for equipment in internalGrid['Creature']['equipment'] if equipment]
                    internalGrid['Creature']['inventory'] = [inventory.__dict__ for inventory in internalGrid['Creature']['inventory'] if inventory]
                    internalGrid['Creature']['drop_table'] = list(internalGrid['Creature']['drop_table'])
                    for k in range(len(internalGrid['Creature']['drop_table'])):
                        if type(internalGrid['Creature']['drop_table'][k]) != type(0.7):
                            internalGrid['Creature']['drop_table'][k] = internalGrid['Creature']['drop_table'][k].__dict__
                    
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

#funtion to process the acttack action
def process_attack(attacker, target):
    
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
            target.die(game_map,get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Creature"),Corpse(target.pos,target.hp,target.damage_resistances))
            if target.name == "Player":
                global gameOver
                gameOver = True
            else:
                return "target killed"
                
        return "target hit"
    else:
        return "target missed"
    
def find_current_level(game_map):
    for x, row in enumerate(game_map):
        for y, tile in enumerate(row):
            for gameObject in (tile):
                if gameObject.name == "Stairs":
                    return gameObject.hp
    return None  # If player is not found
if (HTTP_FIELDS.getvalue('uuid')):
      uuid = HTTP_FIELDS.getvalue('uuid')
      direction = None
      attack = [int(coordinate) for coordinate in HTTP_FIELDS.getvalue('attack').split(",")] if HTTP_FIELDS.getvalue('attack') else None
      difficulty = HTTP_FIELDS.getvalue('difficulty') if (HTTP_FIELDS.getvalue('difficulty')) else "Easy"
      selected = HTTP_FIELDS.getvalue('selected') if (HTTP_FIELDS.getvalue('selected')) else False
      level = HTTP_FIELDS.getvalue('level') if (HTTP_FIELDS.getvalue('level') and uuid == "Test") else "0"
      if (uuid == "Test"):
          difficulty = "Test"
    # Load the current map
      file_path = '../maps/'+uuid+'.pkl' 
      if (not os.path.exists(file_path)):
          game_map = generateMap(0, level+","+difficulty)
          turn_log.append({"level":level+","+difficulty})
          game_log += "New Level Generated "+level+","+difficulty+"\n"
          if (int(level) == 23):
              gameOver = True
      else:
          game_map = load_map(file_path)
      
    # Process player's movement
      message = None
      player_pos = find_player_position(game_map)
      if (attack != None):
          target_coordinates = get_target_tile(attack)
          player = get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Creature")
          direction = get_direction_from_step(player_pos, target_coordinates)
          if (direction == 270):
             player.textureIndex = 36
          elif (direction == 0):
             player.textureIndex = 37
          elif (direction == 90):
             player.textureIndex = 38
          elif (direction == 180):
             player.textureIndex = 39
          
          if (not selected and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Creature") != None and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Creature").name != "Player"): #attack when the target is a creature but not player
              target_coordinates = get_target_tile(attack)
              target_creature = get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Creature")
              if (target_creature):
                  message = process_attack(get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Creature"), target_creature)
                  update_Creature_position(game_map, player_pos)
              else:
                  message = "no target at this position"
                
          elif (not selected and  get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Creature") == None): #move
             
              if (abs(player_pos[0] - target_coordinates[0]) + abs(player_pos[1] - target_coordinates[1]) == 1):
                  
                  
                  player_pos, message = process_Creature_movement(player_pos, direction, game_map)
                  
                  
                  if (get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Item")):
                      get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Creature").pickup_item(game_map,get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Item"))

              else:
                  message = "Movement Out Of Range"
          
          if (not selected and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Decor") and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Decor").name != "Stairs" and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Decor").name != "Corpse"): #interact 
              
              get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Decor").on_interact(game_map,get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Creature"))
              
              message = "Creature has moved" if (message == "Creature has moved") else "interacted with"
              game_log += get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Creature").name +" @ "+str(((get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Creature").pos)))+" Interacted With "+get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Decor").name +" @ "+str(((get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Decor").pos)))+"\n"

          if (selected):
              selected_method = selected.split(":")[0]
              selected_index = selected.split(":")[1]
              
              if (selected_method == "Inventory" and get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Creature")):
                  get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Creature").inventory[0].use_effect(game_map,get_object_by_class(game_map[target_coordinates[0]][target_coordinates[1]],"Creature"))

          
      else:
          turn_log.append({"level":find_current_level(game_map)})
          message = "map loaded"
    #update the Creature's position
      if (message == "Creature has moved"):
          update_Creature_position(game_map, player_pos)
          #print(get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Decor").name)
          if get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Decor") and get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Decor").name == "Stairs":
              stair = get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Decor")
              player = get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Creature")
              player.textureIndex = 38
              depth = str(int(stair.hp.split(",")[0]) + 1)+","+stair.hp.split(",")[1]
              game_map = generateMap(0, depth,player)
              turn_log.append({"level":depth})
              message = "New Map: Level "+str(depth)
              player_pos = find_player_position(game_map)
              game_log += "New Level Generated "+depth+"\n"
              if ((int(stair.hp.split(",")[0]) + 1) == 23):
                 gameOver = True
          
              
    # Save the updated map back to the file
      save_map(file_path, game_map)
      
          
    # Caete the subset of the map
      
      map_subset = get_map_subset(player_pos, game_map, fov_radius)

    #send subset_map and message back to client
      
      if (gameOver):
         game_log += "Game Over. Final Score: "+str(get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Creature").xp)
      
      with open("../logs/"+uuid+".txt", "a") as myfile:
         myfile.write(game_log)
         
      if (gameOver):
         import urllib.request
         import urllib.parse
         full_game_log = urllib.request.urlopen('https://fathomless.io/gameOver/?uuid='+urllib.parse.quote_plus(uuid))
         turn_log.append({"type":"game_over","game_log":(full_game_log.read().decode("utf-8"))}) #end the game if the turn_log contain game_over

      response = {
          "message": message if message else "",
          "map_subset": map_subset,
          "turn_log": turn_log
      }
      sys.stdout.write(json.dumps(response))
      
