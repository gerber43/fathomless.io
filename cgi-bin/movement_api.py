#!/usr/bin/python3
import sys
import json
import cgi
import os
import pickle
from map_simplifier import delete_blank_object
from user_tracking import a_star
from GameObject import Terrain
from Creatures import Goblin, Player
from MasterGenerator import generateMap
from Terrain import Wall, Pit, Water, Fire, Spikes, EmptySpace  
print('Content-type: application/json\n')
HTTP_FIELDS = cgi.FieldStorage()
depth = 0

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
    elif direction == None: #initialization case
        return position, "Map Retrieved"
    else:
        return position, "Invalid direction"
    # Validate the new position
    if not is_valid_move(new_x, new_y, game_map):
        return position, "You cannot move here"  # Invalid move
    
    # Update the Creature's position in the map
    
    message = "Creature has moved"
    get_object_by_class(game_map[x][y],"Creature").move(game_map,[new_x, new_y])
    return (new_x, new_y), message

# Function to update all Creature positions
def update_Creature_position(game_map, player_pos):
    
    moved_Creatures = set()  # Track Creatures that have already moved
    
    for x, row in enumerate(game_map):
        for y, tile in enumerate(row):
            Creature = get_object_by_class(game_map[x][y],"Creature")
            manhattan = abs(player_pos[0] - x) + abs(player_pos[1] - y)
            check = 3
            
            if Creature != None and manhattan < check and Creature.name != "Player":  # if Creature exist and not player
                
                # Check if this Creature has already moved in this turn
                if (x, y) in moved_Creatures:
                    continue
                
                speed = 1
                path = a_star((x, y), player_pos, game_map)

                if not path or len(path) < 2:
                    continue
                
                current_pos = (x, y)
                for move_num in range(min(speed, len(path) - 1)):
                    next_pos = path[move_num + 1]
                    direction = get_direction_from_step(current_pos, next_pos)  # Get direction for the move
                    current_pos, message = process_Creature_movement(current_pos, direction, game_map)
                    if message != "Creature has moved":
                        break
                moved_Creatures.add(current_pos)

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
                    internalGrid['Creature']['equipment'] = [equipment.__dict__ for equipment in internalGrid['Creature']['equipment'] if equipment]
                    internalGrid['Creature']['drop_table'] = list(internalGrid['Creature']['drop_table'])
                    for k in range(len(internalGrid['Creature']['drop_table'])):
                        if type(internalGrid['Creature']['drop_table'][k]) != type(0.7):
                            internalGrid['Creature']['drop_table'][k] = internalGrid['Creature']['drop_table'][k].__dict__
                    
                row_subset.append(internalGrid)
        map_subset.append(row_subset)
    
        
    
    return map_subset
    
    
#Function to get the target creature
def get_target_creature(game_map, player_pos, tile, fov_radius):
    player_x, player_y = player_pos
    fov_x_start = player_x - fov_radius
    fov_y_start = player_y - fov_radius
    target_x = fov_x_start + tile[0]
    target_y = fov_y_start + tile[1]
    if target_x < 0 or target_x >= len(game_map) or target_y < 0 or target_y >= len(game_map[0]):
        return None
    return get_object_by_class(game_map[target_x][target_y],"Creature")

#funtion to process the acttack action
def process_attack(attacker, target, attack_method = None):
    # calculate the damage based on attack_method, now just set to 1
    if (attack_method == None):
        damage = 1
    # reduce target's hp
    target.hp -= damage

    #check did the creature dead
    if target.hp <= 0:
        if target.name == Player:
            return "game over"
        else:
            game_map[target.pos[0]][target.pos[1]].remove(target)
            return "target killed"
            #replace with actual death target
    return "target hit"
    
    
if (HTTP_FIELDS.getvalue('uuid')):
      uuid = HTTP_FIELDS.getvalue('uuid')
      direction = int(HTTP_FIELDS.getvalue('direction')) if (HTTP_FIELDS.getvalue('direction')) else None
      attack = HTTP_FIELDS.getvalue('attack').split(",") if HTTP_FIELDS.getvalue('attack') else None
      difficulty = HTTP_FIELDS.getvalue('difficulty') if (HTTP_FIELDS.getvalue('difficulty')) else None

    
    # Load the current map
      file_path = '../maps/'+uuid+'.pkl' 
      if (not os.path.exists(file_path)):
          game_map = generateMap(0, "0,"+difficulty)
      else:
          game_map = load_map(file_path)
      
    # Process player's movement
      player_pos = find_player_position(game_map)
      if (player_pos != None):
          if (direction != None):
              new_player_pos, message = process_Creature_movement(player_pos, direction, game_map)

          elif (attack != None):
              attack  = [int(coordinate) for coordinate in attack]
              field_of_view = 11
              fov_radius = field_of_view // 2
              target_creature = get_target_creature(game_map, player_pos, attack, fov_radius)
              if (target_creature):
                  message = process_attack(get_object_by_class(game_map[player_pos[0]][player_pos[1]],"Creature"), target_creature)
                  #delete_blank_object(game_map)
              else:
                  message = "no target at this position"
          else:
              message = "invalide action"
      else:
          message = "player not found"
    #update the Creature's position
    
      
      if (message == "Creature has moved"):
          update_Creature_position(game_map, player_pos)
          if get_object_by_class(game_map[new_player_pos[0]][new_player_pos[1]],"Decor") and get_object_by_class(game_map[new_player_pos[0]][new_player_pos[1]],"Decor").name == "Stairs":
              stair = get_object_by_class(game_map[new_player_pos[0]][new_player_pos[1]],"Decor")
              player = get_object_by_class(game_map[new_player_pos[0]][new_player_pos[1]],"Creature")
              
              depth = str(int(stair.hp.split(",")[0]) + 1)+","+stair.hp.split(",")[1]
              game_map = generateMap(0, depth)
    
              message = "New Map: Level "+str(depth)
              new_player_pos = find_player_position(game_map)
              player.pos = [new_player_pos[1],new_player_pos[0]]
          
              
          player_pos = new_player_pos

    # Save the updated map back to the file
      save_map(file_path, game_map)
      
          
    # Caete the subset of the map
      field_of_view = 11
      fov_radius = field_of_view // 2
      map_subset = get_map_subset(player_pos, game_map, fov_radius)

    #send subset_map and message back to client
      response = {
          "message": message,
          "map_subset": map_subset
      }

      sys.stdout.write(json.dumps(response))
