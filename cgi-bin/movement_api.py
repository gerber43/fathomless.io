#!/usr/bin/python3
import sys
import json
import cgi
import os
from user_tracking import a_star
from GameObject import Terrain
from Creatures import Goblin, Player

from Terrain import Wall, Pit, Water, Fire, Spikes, EmptySpace  
print('Content-type: application/json\n')
HTTP_FIELDS = cgi.FieldStorage()
depth = 0
#Function to validate the player session
def validate_session(uuid):
    # TODO
    return True

#Function to load the map file
def load_map(map_file_path):
    with open(map_file_path, 'r') as file:
        return json.load(file)

#Funciton to save the updated map
def save_map(map_file_path, map_data):
    with open(map_file_path, 'w') as file:
        json.dump(map_data, file)

# Function to find the player's current position on the map
def find_player_position(game_map):
    for x, row in enumerate(game_map):
        
        for y, tile in enumerate(row):
            if tile.get('creature') != None and tile.get('creature')['textureIndex'] == "0":
                return (x, y)
    return None  # If player is not found

# Function to process creature's movement
def process_creature_movement(position, direction, game_map):
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
    
    # Update the creature's position in the map
    game_map[new_x][new_y]['creature'] = game_map[x][y]['creature']  # Move creature to new position
    game_map[new_x][new_y]['creature']['pos'] = [new_y,new_x]
    game_map[x][y]['creature'] = {"textureIndex": "8"}  # Clear old position
    message = "creature has moved"
    if (game_map[new_x][new_y]['terrain']['name'] == "Fire"):
        game_map[new_x][new_y]['creature']['hp'] = game_map[new_x][new_y]['creature']['hp'] - 1
        message = "Current HP "+str(game_map[new_x][new_y]['creature']['hp'])
    
    return (new_x, new_y), message

# Function to update all creature positions
def update_creature_position(game_map, player_pos):
    moved_creatures = set()  # Track creatures that have already moved
    for x, row in enumerate(game_map):
        for y, tile in enumerate(row):
            creature = tile.get("creature")
            
            if creature and creature['textureIndex'] != '0' and creature['textureIndex'] != 8 and creature['textureIndex'] != '8':  # if creature exist and not player
                
                # Check if this creature has already moved in this turn
                if (x, y) in moved_creatures:
                    continue
                
                speed = 1
                path = a_star((x, y), player_pos, game_map)
                
                if not path or len(path) < 2:
                    continue

                current_pos = (x, y)
                for move_num in range(min(speed, len(path) - 1)):
                    next_pos = path[move_num + 1]
                    direction = get_direction_from_step(current_pos, next_pos)  # Get direction for the move
                    current_pos, message = process_creature_movement(current_pos, direction, game_map)
                    if message != "creature has moved":
                        break
                moved_creatures.add(current_pos)

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
    if x < 0 or y < 0 or x >= len(game_map) or y >= len(game_map[x]) or game_map[x][y]['creature']['textureIndex'] == '0' or (game_map[x][y]['terrain']['passable'] == False and game_map[x][y].get('decor') is None):
        return False
    return True

#Function to create the subset of map
def get_map_subset(player_pos, game_map, fov_radius):
    x, y = player_pos
    x_max = len(game_map)
    y_max = 0;
    if x_max > 0:
        y_max = len(game_map[0])

    blank_tile = {
        "terrain": {"textureIndex": 8},
        "item": {"textureIndex": 8},
        "decor": {"textureIndex": 8},
        "creature": {"textureIndex": 8},
        "light": {"textureIndex": 8}
    }


    map_subset = []
    for i in range(x - fov_radius, x + fov_radius + 1):
        row_subset = []
        for j in range(y- fov_radius, y + fov_radius + 1):
            if i < 0 or i >= x_max or j < 0  or j >= y_max:
                row_subset.append(blank_tile)
            else:
                row_subset.append(game_map[i][j])
        map_subset.append(row_subset)

    return map_subset
    

try:
    # Retrieve uuid and direction from the POST request
    
    if (HTTP_FIELDS.getvalue('uuid')):
      uuid = HTTP_FIELDS.getvalue('uuid')
      direction = int(HTTP_FIELDS.getvalue('direction')) if (HTTP_FIELDS.getvalue('direction')) else None
      
      
    # Validate session
      if not validate_session(uuid):
           raise ValueError("Invalid session")
      
    # Load the current map
      map_file_path = '../maps/'+uuid+'.json' # will be adjust to the actuall file path later
      
      if (not os.path.exists(map_file_path)):
          from MasterGenerator import generateMap
          generateMap(0,uuid,0)
      
      game_map = load_map(map_file_path)
      
    # Process player's movement
      player_pos = find_player_position(game_map)
      
      if (player_pos != None):
          
          new_player_pos, message = process_creature_movement(player_pos, direction, game_map)
      else:
          message = "player not found"
    


    #update the creature's position
      if (message == "orientation has changed" or message == "creature has moved"):
          update_creature_position(game_map, player_pos)
      if (game_map[new_player_pos[0]][new_player_pos[1]].get('decor') and game_map[new_player_pos[0]][new_player_pos[1]]['decor']['name'] == "Stairs"):
          player = game_map[new_player_pos[0]][new_player_pos[1]]['creature']
          from MasterGenerator import generateMap
          depth = game_map[new_player_pos[0]][new_player_pos[1]]['decor']['hp'] + 1
          
          generateMap(2 if (depth % 2 == 0) else 0,uuid, depth)
          
          game_map = load_map(map_file_path)
          message = "New Map"
          new_player_pos = find_player_position(game_map)
          player['pos']=[new_player_pos[1],new_player_pos[0]]
          game_map[new_player_pos[0]][new_player_pos[1]]['creature'] = player
      
    # Save the updated map back to the file
      save_map(map_file_path, game_map)
      
          

    # Caete the subset of the map
      field_of_view = 11
      fov_radius = field_of_view // 2
      map_subset = get_map_subset(new_player_pos, game_map, fov_radius)


    #send subset_map and message back to client
      response = {
          "message": message,
          "map_subset": map_subset
      }

      sys.stdout.write(json.dumps(response))

except Exception as e:
    print(json.dumps({"error": str(e)}))
