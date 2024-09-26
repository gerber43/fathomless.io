#!/usr/bin/python2
import sys
import json
import cgi
print('Content-type: application/json\n')
HTTP_FIELDS = cgi.FieldStorage()

#Function to validate the player session
def validate_session(session_id):
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
            entity = tile.get('entity')
            if entity and entity['textureIndex'] == 0:
                return (x, y)
    return None  # If player is not found

# Function to process entity's movement
def process_entity_movement(position, direction, game_map):
    x, y = position
    current_rotation = game_map[x][y]['entity']['rotation']

    # If the entity is not facing the correct direction, just update the rotation
    if current_rotation != direction:
        game_map[x][y]['entity']['rotation'] = direction  # Change the rotation
        return position, "orientation has changed"

    # If the entity is facing the correct direction, calculate the new position
    if direction == 0:  # Move right
        new_x, new_y = x + 1, y
    elif direction == 90:  # Move up
        new_x, new_y = x, y - 1
    elif direction == 180:  # Move left
        new_x, new_y = x - 1, y
    elif direction == 270:  # Move down
        new_x, new_y = x, y + 1
    else:
        return position, "Invalid direction"

    # Validate the new position
    if not is_valid_move(new_x, new_y, game_map):
        return position, "You cannot move here"  # Invalid move

    # Update the entity's position in the map
    game_map[new_x][new_y]['entity'] = game_map[x][y]['entity']  # Move entity to new position
    game_map[x][y]['entity'] = None  # Clear old position

    return (new_x, new_y), "entity has moved"

# Function to update all entity positions
def update_entity_position(game_map):
    for x, row in enumerate(game_map):
        for y, tile in enumerate(row):
            entity = tile.get("entity")
            if entity:
                direction = get_direction(entity) #the pathfinding algorithm to be implement later
                process_entity_movement((x,y), direction, game_map)

# Function to validate the movement
def is_valid_move(x, y, game_map):
    if x < 0 or y < 0 or x >= len(game_map) or y >= len(game_map[x]):
        return False
    if game_map[y][x].get('obstacle'):
        return False
    return True

#Function to create the subset of map
def get_map_subset(player_pos, game_map, fov_radius):
    x, y = player_pos
    x_max = len(game_map)
    y_max = 0;
    if x_max > 0:
        y_max = len(game_map[0])

    balnk_tile = {
        "tile": {"textureIndex": 8, "rotation": 0},
        "item": {"textureIndex": 8, "rotation": 0},
        "obstacle": {"textureIndex": 8, "rotation": 0},
        "entity": {"textureIndex": "8", "rotation": "0"}
    }


    map_subset = []
    for i in range(x - fov_radius, x + fov_radius + 1):
        row_subset = []
        for j in range(y- fov_radius, y + fov_radius + 1):
            if i < 0 or i >= x_max or j < 0  or j >= y_max:
                row_subset.append(balnk_tile)
            else:
                row_subset.append(game_map[i][j])
        map_subset.append(row_subset)

    return map_subset

# Function to save the map subset to a separate file
def save_map_subset(subset_file_path, map_subset):
    with open(subset_file_path, 'w') as file:
        json.dump(map_subset, file)

try:
    # Retrieve session_id and direction from the POST request
    session_id = HTTP_FIELDS.getvalue('session_id')
    direction = int(HTTP_FIELDS.getvalue('direction'))

    # Validate session
    if not validate_session(session_id):
         raise ValueError("Invalid session")

    # Load the current map
    map_file_path = 'map.json' # will be adjust to the actuall file path later
    game_map = load_map(map_file_path)

    # Process player's movement
    player_pos = find_player_position(game_map);
    new_player_pos, message = process_player_movement(player_pos, direction, game_map)

    #update the entity's position
    update_entity_position(game_map)

    # Save the updated map back to the file
    save_map(map_file_path, game_map)

    # Caete the subset of the map
    field_of_view = 5
    fov_radis = field_of_view // 2
    map_subset = get_map_subset(new_player_pos, game_map, fov_radius)

    # Save the subset into a separate file (map_subset.json)
    subset_file_path = 'map_subset.json' #tbd later
    save_map_subset(subset_file_path, map_subset)

    #send subset_map and message back to client
    response = {
        "message": message,
        "map_subset": map_subset
    }

    sys.stdout.write(json.dumps(response))

except Exception as e:
    print(json.dumps({"error": str(e)}))








