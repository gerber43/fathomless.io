#!/usr/bin/python3
import sys
import json
import cgi
import random

HTTP_FIELDS = cgi.FieldStorage()

from GameObject import Terrain, Decor, Creature
from Terrain import Wall, Pit, Water, Fire, Spikes, EmptySpace  
from Decor import Stairs, Door
from Creatures import Player, Goblin, Spider, Bat, Fishman, UndeadSailor, Pirate, GoblinMiner, RockWorm, GiantSlime, SewerGator, DiseasedDenizen, BloatedScavenger, MagmaGolem, FireElemental, DarkElf, DarkDwarf, XotilWarrior, XotilAbomination, XotilHighPriest, AshGolem, ObsidianGolem, AshGhoul, AshWight, SkeletonSoldier, WraithLeader, FleshGolem, Polyp, Parasite, BloodCrawler, Liche, DeathKnight, Archdemon, Demon, NewGodServant, MistBeast, OldGodCultist, EldritchMinion,  VoidBeast, CosmicDragon


biomes = {
    1: [Goblin, Spider, Bat],             # Cave creatures
    2: [Goblin, Spider, Bat],             # Cave creatures
    3: [Fishman, UndeadSailor, Pirate],   # Cove creatures
    4: [GoblinMiner, RockWorm],           # Mine creatures
    5: [GoblinMiner, RockWorm],           # Mine creatures
    6: [GiantSlime, SewerGator],          # Sewer creatures
    7: [GiantSlime, SewerGator],          # Sewer creatures
    8: [DiseasedDenizen, BloatedScavenger],  # Shantytown creatures
    9: [MagmaGolem, FireElemental],       # Magma Core creatures
    10: [DarkElf, DarkDwarf],              # Deep Cave creatures
    11: [XotilWarrior, XotilAbomination, XotilHighPriest],  # Ziggurat creatures
    12: [AshGolem, ObsidianGolem],         # Ember creatures
    13: [AshGhoul, AshWight],             # Columbarium creatures
    14: [SkeletonSoldier, WraithLeader],  # Catacomb creatures
    15: [FleshGolem, Polyp],              # Carrion creatures
    16: [Parasite, BloodCrawler],         # Worldeater’s Gut creatures
    17: [Liche, DeathKnight],             # Necropolis creatures
    18: [Archdemon, Demon],               # Underworld creatures
    19: [NewGodServant, MistBeast],       # Ancient City creatures
    20: [OldGodCultist, EldritchMinion],  # Temple of the Old One creatures
    21: [VoidBeast],                      # Cosmic Void creatures
    22: [CosmicDragon],                   # Heart of the World (Final Boss)
}


def is_within_grid(x, y, width, height):
    return 0 <= x < width and 0 <= y < height

def add_spike_line(grid, x1, y1, length, direction):
    width = len(grid[0])
    height = len(grid)

    if direction == 'horizontal':
        for x in range(x1, min(x1 + length, width)):  
            if is_within_grid(x, y1, width, height):
                # Remove existing terrain before adding spikes
                grid[y1][x] = [obj for obj in grid[y1][x] if not isinstance(obj, Terrain)]
                grid[y1][x].append(Spikes((y1, x)))  
    elif direction == 'vertical':
        for y in range(y1, min(y1 + length, height)):  
            if is_within_grid(x1, y, width, height):
                grid[y][x1] = [obj for obj in grid[y][x1] if not isinstance(obj, Terrain)]
                grid[y][x1].append(Spikes((y, x1)))  

def add_walls(grid, x1, y1, x2, y2):
    width = len(grid[0])
    height = len(grid)
    x1, x2 = max(0, x1), min(x2, width - 1)
    y1, y2 = max(0, y1), min(y2, height - 1)
    
    for x in range(x1, x2 + 1):
        if is_within_grid(x, y1, width, height):
            # Remove existing terrain before adding Wall
            grid[y1][x] = [obj for obj in grid[y1][x] if not isinstance(obj, Terrain)]
            grid[y1][x].append(Wall((y1, x)))  
        if is_within_grid(x, y2, width, height):
            grid[y2][x] = [obj for obj in grid[y2][x] if not isinstance(obj, Terrain)]
            grid[y2][x].append(Wall((y2, x)))
    
    for y in range(y1, y2 + 1):
        if is_within_grid(x1, y, width, height):
            grid[y][x1] = [obj for obj in grid[y][x1] if not isinstance(obj, Terrain)]
            grid[y][x1].append(Wall((y, x1)))
        if is_within_grid(x2, y, width, height):
            grid[y][x2] = [obj for obj in grid[y][x2] if not isinstance(obj, Terrain)]
            grid[y][x2].append(Wall((y, x2)))

# Filled rectangle grid placement for water and fire Terrain 
def add_filled_rectangle(grid, x1, y1, x2, y2, terrain_class):
    width = len(grid[0])
    height = len(grid)
    x1, x2 = max(0, x1), min(x2, width - 1)
    y1, y2 = max(0, y1), min(y2, height - 1)

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if is_within_grid(x, y, width, height):
                # Remove existing terrain before adding the new terrain object
                grid[y][x] = [obj for obj in grid[y][x] if not isinstance(obj, Terrain)]
                grid[y][x].append(terrain_class((y, x)))  

def add_random_pits(grid, num_pits, width, height):
    for _ in range(num_pits):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if is_within_grid(x, y, width, height):
            grid[y][x] = [obj for obj in grid[y][x] if not isinstance(obj, Terrain)]
            grid[y][x].append(Pit((y, x)))  

def add_random_empty(grid, num_empty, width, height):
    for _ in range(num_empty):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if is_within_grid(x, y, width, height):
            grid[y][x].append(EmptySpace((y, x)))
def place_doors(grid, width, height, door_probability=0.6):
    for y in range(1, height - 1):  # Iterate through the grid, avoiding the borders
        for x in range(1, width - 1):
            # Ensure the current tile is a Wall
            if any(isinstance(obj, Wall) for obj in grid[y][x]):
                # Check the four possible adjacent tiles
                left = grid[y][x-1]
                right = grid[y][x+1]
                top = grid[y-1][x]
                bottom = grid[y+1][x]
                # Ensure there's no adjacent door
                adjacent_tiles = [left, right, top, bottom]
                if any(any(isinstance(obj, Door) for obj in tile) for tile in adjacent_tiles):
                    continue  # Skip this tile if there is an adjacent door
                # Check for exactly 2 free spaces, either horizontally (left-right) or vertically (top-bottom)
                if (any(isinstance(obj, EmptySpace) for obj in left) and any(isinstance(obj, EmptySpace) for obj in right)) or \
                   (any(isinstance(obj, EmptySpace) for obj in top) and any(isinstance(obj, EmptySpace) for obj in bottom)):
                    # Introduce 60% chance of placing the door
                    if random.random() < door_probability:
                        # Remove the wall and place a door
                        #grid[y][x] = [obj for obj in grid[y][x] if not isinstance(obj, Wall)]  # Remove the wall
                        grid[y][x].append(Door((y, x)))
                        
def place_creatures(grid, num_creatures, depth):
    current_biome = int(depth.split(",")[0])

    if current_biome in biomes:
        available_creatures = biomes[current_biome]
        
        for _ in range(num_creatures):
            while True:
                x = random.randint(0, len(grid) - 1)
                y = random.randint(0, len(grid[0]) - 1)
                if any(isinstance(obj, EmptySpace) for obj in grid[y][x]) and not any(isinstance(obj, Creature) for obj in grid[y][x]):
                    CreatureClass = random.choice(available_creatures)
                    creature = CreatureClass((y, x))
                    creature.hp += current_biome  
                    grid[y][x].append(creature)
                    break

def place_player(grid):
    while True:
        x = random.randint(0, len(grid) - 1)
        y = random.randint(0, len(grid[0]) - 1)
        # Check if the current cell contains EmptySpace and no creature yet
        if any(isinstance(obj, EmptySpace) for obj in grid[y][x]) and not any(isinstance(obj, Creature) for obj in grid[y][x]):
            grid[y][x].append(Player((y, x)))
            break

def fill_empty_spaces(grid):
    width = len(grid[0])
    height = len(grid)
    
    for y in range(height):
        for x in range(width):
            if not grid[y][x]:
                grid[y][x].append(EmptySpace((y, x)))
def place_staircase(grid, traversable_path,depth):
    # Randomly select a position from the traversable path
    staircase_position = random.choice(list(traversable_path))
    # Get the x, y position for the staircase
    x, y = staircase_position
    # Append the staircase to the space without removing the terrain
    stairs = Stairs((y, x))
    stairs.hp = depth
    grid[y][x].append(stairs)


# Carve a guaranteed path between sides of the map
def carve_path(grid, start, end):
    current = start
    visited = set()
    visited.add(current)
    x, y = current
    x_goal, y_goal = end
    # Continue carving the path until we reach the end
    while current != end:
        # Replace any existing terrain with free space
        grid[y][x] = [obj for obj in grid[y][x] if not isinstance(obj, Terrain)]
        grid[y][x].append(EmptySpace((y, x)))  # Carve out free space
        # Determine direction towards the goal
        x_dir = 1 if x_goal > x else -1 if x_goal < x else 0
        y_dir = 1 if y_goal > y else -1 if y_goal < y else 0
        # Create a bias for moving towards the destination with some variation
        next_steps = []
        if x_dir != 0:
            next_steps.append((y ,x + x_dir))  # Move horizontally towards the goal
        if y_dir != 0:
            next_steps.append((y + y_dir, x))  # Move vertically towards the goal
        # Add small side variations but limit them
        if x_dir != 0:  # Horizontal movement allowed
            next_steps.append((y + random.choice([-1, 0, 1]), x + x_dir))  # Slight vertical deviation
        if y_dir != 0:  # Vertical movement allowed
            next_steps.append((y + y_dir, x + random.choice([-1, 0, 1])))  # Slight horizontal deviation
        # Filter valid next steps (within bounds and not visited)
        valid_next_steps = [(nx, ny) for nx, ny in next_steps
                            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid)
                            and (nx, ny) not in visited]
        # If no valid steps, break (this shouldn't usually happen)
        if not valid_next_steps:
            break
        # Randomly choose one of the valid steps
        current = random.choice(valid_next_steps)
        x, y = current
        visited.add(current)
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

    # Combine paths and replace with free spaces
    traversable_path = top_bottom_path.union(left_right_path)

    for pos in traversable_path:
        x, y = pos
        grid[y][x] = [obj for obj in grid[y][x] if not isinstance(obj, Terrain)]  # Remove terrain
        grid[y][x].append(EmptySpace((y, x)))  # Replace with free space
    return grid, traversable_path






# Main map generation function
def generate_terrain_with_probabilities(grid_width, grid_height, terrain_probabilities):
    grid = [[[] for _ in range(grid_width)] for _ in range(grid_height)]

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
# def print_final_grid(grid):
#     for row in grid:
#         row_symbols = []
#         for cell in row:
#             # Gather the symbols for each GameObject in the cell
#             symbols = [obj.symbol for obj in cell]
#             row_symbols.append(f"[{', '.join(symbols)}]")
#         print(" ".join(row_symbols))
# # Print the final grid
# print_final_grid(final_grid)
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



    # Define probabilities for each terrain type

texture_mapping = {
    'EmptySpace': 1,
    'Water': 2,
    'Fire': 4,
    'Spikes': 17,
    'Pit': 18,
    'Wall': 6,  
}
def generateMap(width, height, depth, num_creatures):
    # Generate terrain grid with probabilities
    terrain_probabilities = {
    'walls': 0.2,
    'spikes': 0.1,
    'water': 0.08,
    'fire': 0.08,
    'pits': 0.03,
    'empty_space': 0.5
    }
    terrain_grid = generate_terrain_with_probabilities(width, height, terrain_probabilities)
    
    place_creatures(terrain_grid, num_creatures, depth)
    
    place_doors(terrain_grid, width, height)
    
    # Carve guaranteed paths across the grid
    final_grid, final_traversable_grid = carve_guaranteed_paths(terrain_grid, width, height)
    
    place_staircase(final_grid, final_traversable_grid,depth)
    
    place_player(final_grid)

    return final_grid
    #json_map = convert_grid_to_json(final_grid)
    # Convert the map to JSON format and print
    #json_output = json.dumps(json_map)
    #print(json_output)

    # save the output to a file
    #with open("../maps/"+uuid+".json", "w") as json_file:
        #json_file.write(json_output)
