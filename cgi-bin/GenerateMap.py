import random

from GameObject import *
from Terrain import *  
from Decor import *
from Creatures import *
from Items import *
from Biomes import *


caves = Caves()
cove = Cove()
mine = Mine()
corruptite_mine = CorruptiteMine()
sewer = Sewer()
shantytown = Shantytown()
magma_core = MagmaCore()
deep_cavern = DeepCavern()
ziggurat = Ziggurat()
embers = Embers()
undercity = Undercity()
columbarium = Columbarium()
catacomb = Catacomb()
carrion = Carrion()
worldeaters_gut = WorldeatersGut()
necropolis = Necropolis()
underworld1 = Underworld1()
underworld2 = Underworld2()
underworld3 = Underworld3()
underworld4 = Underworld4()
underworld5 = Underworld5()
ancient_city = AncientCity()
old_temple = OldTemple()
cosmic_void = CosmicVoid()
world_heart = WorldHeart()

biomes_dict = {
    0: caves,
    1: caves,            
    2: caves,            
    3: cove,             
    4: mine,            
    5: corruptite_mine,  
    6: sewer,            
    7: sewer,            
    8: shantytown,       
    9: magma_core,       
    10: deep_cavern,     
    11: ziggurat,        
    12: embers,          
    13: columbarium,     
    14: catacomb,        
    15: carrion,         
    16: worldeaters_gut, 
    17: necropolis,      
    18: underworld1,     
    19: ancient_city,    
    20: old_temple,      
    21: cosmic_void,     
    22: world_heart,
    23: world_heart  
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


def place_player(grid, player, traversable_path, times = 0):
    y, x = random.choice(list(traversable_path))

    if any(isinstance(obj, EmptySpace) for obj in grid[y][x]) and not any(isinstance(obj, Creature) for obj in grid[y][x]) and not any(isinstance(obj, Decor) for obj in grid[y][x]):
        player.pos = [y, x]
        grid[y][x].append(player)
    else:
        if (times < len(traversable_path)):
            place_player(grid, player, traversable_path, times + 1)
        else:
            grid[y][x] = []
            player.pos = [y, x]
            grid[y][x].append(player)
            

def fill_empty_spaces(grid):
    width = len(grid[0])
    height = len(grid)
    
    for y in range(height):
        for x in range(width):
            if not grid[y][x]:
                grid[y][x].append(EmptySpace((y, x)))
def place_staircase(grid, traversable_path,depth):
    
    for i in range(random.randint(1, 3)):
        # Randomly select a position from the traversable path
        staircase_position = random.choice(list(traversable_path))
        # Get the x, y position for the staircase
        x, y = staircase_position
        # Append the staircase to the space without removing the terrain
        stairs = Stairs((y, x))
        stairs.hp = depth
        grid[y][x].append(stairs)

def place_items_with_biome(grid, biome, num_items):
    width = len(grid[0])
    height = len(grid)
    for _ in range(num_items):
        while True:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            if any(isinstance(obj, EmptySpace) for obj in grid[y][x]) and not any(isinstance(obj, Item) for obj in grid[y][x]):
                # Use biome's random_other method to generate an item
                item = biome.random_other()
                item = eval(item)((y,x))
                if item and not isinstance(item, (Door, Pit)): 
                    grid[y][x].append(item)
                break

def place_decor(grid, biome, width, height):
        other_spawns = biome.other_spawns
        other_weights = biome.other_weights
        for y in range(height):
            for x in range(width):
                if any(isinstance(obj, EmptySpace) for obj in grid[y][x]):
                    for i in range(len(other_spawns)):
                        decor_type = other_spawns[i]
                        probability = other_weights[i]
                        if random.random() < probability:
                            decor_class = globals().get(decor_type)  
                            if decor_class:
                                decor_item = decor_class((y, x))
                                
                                grid[y][x].append(decor_item)
                                break  # Place one decor per tile
    
def place_creatures_by_biome(grid, biome, num_creatures):
    for _ in range(num_creatures):
        creature_type = random.choices(biome.creature_spawns, biome.creature_weights)[0]
        counter = 0
        while True:
            x, y = random.randint(0, len(grid) - 1), random.randint(0, len(grid[0]) - 1)
            forceCreature = False
            if counter > len(grid)*len(grid[0]) and not any(isinstance(obj, Stairs) for obj in grid[y][x]):
                forceCreature = True
            if len(grid[y][x]) != 0:
                creature = eval(creature_type)((y, x))
                placeCreature = True
                for segment in creature.segments:
                    if (0 > segment.pos[1] or segment.pos[1] >= len(grid) or 0 > segment.pos[0] or segment.pos[0] >= len(grid)) or len(grid[segment.pos[1]][segment.pos[0]]) != 0:
                        placeCreature = False
                        if forceCreature and any(isinstance(obj, Stairs) for obj in grid[y][x]):
                            forceCreature = False
                if placeCreature or forceCreature:
                    if forceCreature:
                        grid[y][x] = []
                    grid[y][x].append(creature)
                    for segment in creature.segments:
                        grid[segment.pos[0]][segment.pos[1]] = [segment]
                        segment.creature = creature
                    break
            counter += 1
            
                

# Carve a guaranteed path between sides of the map
def carve_path(grid, start, end):
    current = start
    visited = set()
    visited.add(current)
    x, y = current
    x_goal, y_goal = end
    # Continue carving the path until we reach the end
    while current != end:
        grid[y][x] = [obj for obj in grid[y][x] if not isinstance(obj, GameObject)]
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
        if x_dir != 0 and random.random() < 0.20:  # 20% chance of jog
            jog_y = y + random.choice([-1, 1])
            if 0 <= jog_y < len(grid):
                next_steps.append((jog_y, x))  # Vertical jog while moving horizontally
        if y_dir != 0 and random.random() < 0.20:  # 20% chance of jog
            jog_x = x + random.choice([-1, 1])
            if 0 <= jog_x < len(grid[0]):
                next_steps.append((y, jog_x))  # Horizontal jog while moving vertically

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
        grid[y][x] = [obj for obj in grid[y][x] if not isinstance(obj, GameObject)]  # Remove terrain
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
def generateMap(width, height, depth, num_creatures, player, num_items):
    depths = depth.split(",")
    current_biome = biomes_dict.get(int(depths[0]))
    if current_biome is None:
        raise ValueError(f"No biome defined for depth {depth}")

    
    terrain_probabilities = {
    'walls': 0.2,
    'spikes': 0.1,
    'water': 0.08,
    'fire': 0.08,
    'pits': 0.5,
    'empty_space': 0.5
    }
    terrain_grid = generate_terrain_with_probabilities(width, height, terrain_probabilities)
        

    #place_decor(terrain_grid, current_biome, width, height)
    
    place_doors(terrain_grid, width, height)
    final_grid, final_traversable_grid = carve_guaranteed_paths(terrain_grid, width, height)
    
    place_staircase(final_grid, final_traversable_grid,depth)
    place_player(final_grid, player, final_traversable_grid)
    place_items_with_biome(final_grid, current_biome, num_items)
    place_creatures_by_biome(terrain_grid, current_biome, num_creatures)
    for i in range(len(final_grid)):
        for j in range(len(final_grid[i])):
            final_grid[i][j].append(Bottom("Bottom", 1,(i,j)))
            
            final_grid[i][j].append(Light((i,j),.4))
            
            for k in range(len(final_grid[i][j])):
                if k < len(final_grid[i][j]) and isinstance(final_grid[i][j][k], EmptySpace):
                    del final_grid[i][j][k]

                
    for i in range(len(final_grid)):
        for j in range(len(final_grid[i])):
            for k in range(len(final_grid[i][j])):
                if hasattr(final_grid[i][j][k], "intensity") and not isinstance(final_grid[i][j][k],Light):
                    spread_light(final_grid, [i,j], final_grid[i][j][k].intensity, [])
    max_light = 0
    for i in range(len(final_grid)):
        for j in range(len(final_grid[i])):
            for k in range(len(final_grid[i][j])):
                if hasattr(final_grid[i][j][k], "intensity") and isinstance(final_grid[i][j][k],Light) and final_grid[i][j][k].intensity > max_light:
                    max_light = final_grid[i][j][k].intensity
    if (max_light > .8):
         for i in range(len(final_grid)):
            for j in range(len(final_grid[i])):
                for k in range(len(final_grid[i][j])):
                    if hasattr(final_grid[i][j][k], "intensity") and isinstance(final_grid[i][j][k],Light):
                        if (final_grid[i][j][k].intensity/max_light > .2):
                            final_grid[i][j][k].intensity = final_grid[i][j][k].intensity/max_light
                        else:
                            final_grid[i][j][k].intensity = .2
        
        
    return final_grid
