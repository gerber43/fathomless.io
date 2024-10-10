#!/usr/bin/python3
import sys
import json
import cgi
import random

HTTP_FIELDS = cgi.FieldStorage()

from GameObject import Terrain

from Terrain import Wall, Pit, Water, Fire, Spikes, EmptySpace  

def is_within_grid(x, y, width, height):
    return 0 <= x < width and 0 <= y < height

def add_spike_line(grid, x1, y1, length, direction):
    width = len(grid[0])
    height = len(grid)

    if direction == 'horizontal':
        for x in range(x1, min(x1 + length, width)):  
            # Check spike line doesn't exceed grid width
            if is_within_grid(x, y1, width, height): 
                grid[y1][x] = Spikes((x, y1))
    elif direction == 'vertical':
        for y in range(y1, min(y1 + length, height)):  
            # Check spike line doesn't exceed grid height
            if is_within_grid(x1, y, width, height):
                grid[y][x1] = Spikes((x1, y))

def add_walls(grid, x1, y1, x2, y2):
    width = len(grid[0])
    height = len(grid)
    x1, x2 = max(0, x1), min(x2, width - 1)
    y1, y2 = max(0, y1), min(y2, height - 1)
    for x in range(x1, x2 + 1):
        if is_within_grid(x, y1, width, height):
            grid[y1][x] = Wall((x, y1))
        if is_within_grid(x, y2, width, height):
            grid[y2][x] = Wall((x, y2))
    for y in range(y1, y2 + 1):
        if is_within_grid(x1, y, width, height):
            grid[y][x1] = Wall((x1, y))
        if is_within_grid(x2, y, width, height):
            grid[y][x2] = Wall((x2, y))

# Filled rectangle grid placement for water and fire Terrain 
def add_filled_rectangle(grid, x1, y1, x2, y2, terrain_class):
    width = len(grid[0])
    height = len(grid)
    x1, x2 = max(0, x1), min(x2, width - 1)
    y1, y2 = max(0, y1), min(y2, height - 1)

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if is_within_grid(x, y, width, height):
                grid[y][x] = terrain_class((x, y))

def add_random_pits(grid, num_pits, width, height):
    for _ in range(num_pits):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if is_within_grid(x, y, width, height):
            grid[y][x] = Pit((x, y))

def add_random_empty(grid, num_empty, width, height):
    for _ in range(num_empty):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if is_within_grid(x, y, width, height):
            grid[y][x] = EmptySpace((x, y))


# Carve a guaranteed path between sides of the map
def carve_path(grid, start, end):
    stack = [start]
    visited = set()
    visited.add(start)
    
    while stack:
        current = stack.pop()
        x, y = current
        if current == end:
            return visited  # Path found
        
        # Shuffle neighbors for randomization
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        random.shuffle(neighbors)
        
        for nx, ny in neighbors:
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if (nx, ny) not in visited and grid[ny][nx] is None:
                    visited.add((nx, ny))
                    stack.append((nx, ny))
    
    return visited  # Return the traversable path

def carve_guaranteed_paths(grid, width, height):
    # Carve path from top to bottom
    top_start = (random.randint(0, width - 1), 0)  
    bottom_end = (random.randint(0, width - 1), height - 1)  
    top_bottom_path = carve_path(grid, top_start, bottom_end)

    # Carve path from left to right
    left_start = (0, random.randint(0, height - 1))  
    right_end = (width - 1, random.randint(0, height - 1))  
    left_right_path = carve_path(grid, left_start, right_end)
    
    
    traversable_path = top_bottom_path.union(left_right_path)

    # Combine paths and clear them
    for pos in top_bottom_path.union(left_right_path):
        x, y = pos
        grid[y][x] = None  # Clear path
    
    return grid, traversable_path

def fill_empty_spaces(grid):
    width = len(grid[0])
    height = len(grid)
    
    for y in range(height):
        for x in range(width):
            if grid[y][x] is None:
                grid[y][x] = EmptySpace((x, y)) 





# Main map generation function
def generate_terrain_with_probabilities(grid_width, grid_height, terrain_probabilities):
    grid = [[None for _ in range(grid_width)] for _ in range(grid_height)]

    for y in range(grid_height):
        for x in range(grid_width):
            # Randomly decide terrain type based on probabilities
            terrain_type = random.choices(
                list(terrain_probabilities.keys()),
                weights=list(terrain_probabilities.values()),
                k=1
            )[0]
            
            # Place terrain based on chosen type
            if terrain_type == 'walls':
                x1, y1 = random.randint(0, grid_width - 5), random.randint(0, grid_height - 5)
                x2, y2 = min(x1 + random.randint(3, 7), grid_width - 1), min(y1 + random.randint(3, 7), grid_height - 1)
                add_walls(grid, x1, y1, x2, y2)
            elif terrain_type == 'spikes':
                x1, y1 = random.randint(0, grid_width - 10), random.randint(0, grid_height - 10)
                length = random.randint(3, 10)
                direction = random.choice(['horizontal', 'vertical'])
                add_spike_line(grid, x1, y1, length, direction)
            elif terrain_type == 'water':
                x1, y1 = random.randint(0, grid_width - 5), random.randint(0, grid_height - 5)
                x2, y2 = min(x1 + random.randint(2, 7), grid_width - 1), min(y1 + random.randint(2, 7), grid_height - 1)
                add_filled_rectangle(grid, x1, y1, x2, y2, Water)
            elif terrain_type == 'fire':
                x1, y1 = random.randint(0, grid_width - 5), random.randint(0, grid_height - 5)
                x2, y2 = min(x1 + random.randint(2, 7), grid_width - 1), min(y1 + random.randint(2, 7), grid_height - 1)
                add_filled_rectangle(grid, x1, y1, x2, y2, Fire)
            elif terrain_type == 'empty_space':
                x1, y1 = random.randint(0, grid_width - 5), random.randint(0, grid_height - 5)
                x2, y2 = min(x1 + random.randint(3, 7), grid_width - 1), min(y1 + random.randint(3, 7), grid_height - 1)
                add_filled_rectangle(grid, x1, y1, x2, y2, EmptySpace)
            elif terrain_type == 'pits':
                add_random_pits(grid, 1, grid_width, grid_height)

    fill_empty_spaces(grid)  
    return grid
def get_texture_index(terrain):
    if isinstance(terrain, EmptySpace):
        return texture_mapping['EmptySpace']
    elif isinstance(terrain, Water):
        return texture_mapping['Water']
    elif isinstance(terrain, Fire):
        return texture_mapping['Fire']
    elif isinstance(terrain, Spikes):
        return texture_mapping['Spikes']
    elif isinstance(terrain, Pit):
        return texture_mapping['Pit']
    elif isinstance(terrain, Wall):
        return texture_mapping['Wall']
    else:
        return texture_mapping['EmptySpace']  # Default to empty space for unknown types


    # Parameters
width = 100
height = 100
    
    # Define probabilities for each terrain type
terrain_probabilities = {
    'walls': 0.2,
    'spikes': 0.1,
    'water': 0.08,
    'fire': 0.08,
    'pits': 0.03,
    'empty_space': 0.5
}
texture_mapping = {
    'EmptySpace': 1,
    'Water': 2,
    'Fire': 4,
    'Spikes': 17,
    'Pit': 18,
    'Wall': 6,  
}
    


def generateMap():
    # Generate terrain grid with probabilities
    terrain_grid = generate_terrain_with_probabilities(width, height, terrain_probabilities)
    # Carve guaranteed paths across the grid
    final_grid, final_traverable_grid = carve_guaranteed_paths(terrain_grid, width, height)
    # Example: Printing the terrain grid
    #for row in final_grid:
    #    print(''.join([terrain.symbol if terrain else '.' for terrain in row]))
    return final_grid
    #json_map = convert_grid_to_json(final_grid)
    # Convert the map to JSON format and print
    #json_output = json.dumps(json_map)
    #print(json_output)
    
    # save the output to a file
    #with open("../maps/"+uuid+".json", "w") as json_file:
        #json_file.write(json_output)
