#!/usr/bin/python3
import sys
import json
import cgi
import random

HTTP_FIELDS = cgi.FieldStorage()

from GameObject import Terrain

from Terrain import Wall, Pit, Water, Fire, Spikes, EmptySpace  

def generate_path_level(width, height, num_paths, spike_prob, water_prob, fire_prob):
    # Initialize grid filled with Wall objects
    grid = [[Wall((x, y)) for x in range(width)] for y in range(height)]
    
    empty_spaces = set()  # To track empty spaces (paths)
    wall_spaces = set()   # To track remaining wall spaces

    # Carve multiple guaranteed paths based on num_paths
    traversable_paths = set()
    for _ in range(num_paths):
        grid, traversable_path = carve_guaranteed_paths(grid, width, height)
        traversable_paths.update(traversable_path)

    # Add spikes, water, and fire based on probabilities
    fill_empty_spaces_with_spikes(grid, traversable_paths, spike_prob)
    fill_walls_with_water_or_fire(grid, width, height, water_prob, fire_prob)

    return grid


def carve_path(grid, start, end, start_side):
    stack = [start]
    visited = set()
    visited.add(start)
    
    while stack:
        current = stack.pop()
        x, y = current
        if current == end:
            return visited  # Path found
        
        # Define allowed directions based on the start side to prevent backtracking
        if start_side == 'top':
            allowed_directions = [(x, y + 1), (x + 1, y), (x - 1, y)]
        elif start_side == 'bottom':
            allowed_directions = [(x, y - 1), (x + 1, y), (x - 1, y)]
        elif start_side == 'left':
            allowed_directions = [(x + 1, y), (x, y + 1), (x, y - 1)]
        else:  # 'right'
            allowed_directions = [(x - 1, y), (x, y + 1), (x, y - 1)]
        
        # Shuffle neighbors for randomization and only allow forward directions
        random.shuffle(allowed_directions)
        
        for nx, ny in allowed_directions:
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if (nx, ny) not in visited and isinstance(grid[ny][nx], Wall):
                    visited.add((nx, ny))
                    stack.append((nx, ny))
                    grid[ny][nx] = EmptySpace((nx, ny))  # Carve path
    
    return visited  # Return the traversable path


def carve_guaranteed_paths(grid, width, height):
    # Randomly select a starting side (top, bottom, left, right) for each path
    start_side = random.choice(['top', 'bottom', 'left', 'right'])
    
    if start_side == 'top':
        start_x = random.randint(0, width - 1)
        start_y = 0
        end_x = random.randint(0, width - 1)
        end_y = height - 1
    elif start_side == 'bottom':
        start_x = random.randint(0, width - 1)
        start_y = height - 1
        end_x = random.randint(0, width - 1)
        end_y = 0
    elif start_side == 'left':
        start_x = 0
        start_y = random.randint(0, height - 1)
        end_x = width - 1
        end_y = random.randint(0, height - 1)
    else:  # 'right'
        start_x = width - 1
        start_y = random.randint(0, height - 1)
        end_x = 0
        end_y = random.randint(0, height - 1)
    
    start = (start_x, start_y)
    end = (end_x, end_y)
    
    # Carve the path and return the set of traversable tiles
    traversable_path = carve_path(grid, start, end, start_side)

    # Expand paths to 3 tiles wide
    expand_path_to_3(grid, traversable_path, width, height)

    return grid, traversable_path


def expand_path_to_3(grid, path, width, height):
    for x, y in path:
        # Expand the path horizontally and vertically to make it 3 tiles wide
        if x + 1 < width and isinstance(grid[y][x + 1], Wall):
            grid[y][x + 1] = EmptySpace((x + 1, y))
        if x - 1 >= 0 and isinstance(grid[y][x - 1], Wall):
            grid[y][x - 1] = EmptySpace((x - 1, y))
        if y + 1 < height and isinstance(grid[y + 1][x], Wall):
            grid[y + 1][x] = EmptySpace((x, y + 1))
        if y - 1 >= 0 and isinstance(grid[y - 1][x], Wall):
            grid[y - 1][x] = EmptySpace((x, y - 1))


def fill_empty_spaces_with_spikes(grid, empty_spaces, spike_prob):
    for (x, y) in empty_spaces:
        if random.random() < spike_prob:
            grid[y][x] = Spikes((x, y))  # Place Spikes in empty spaces


def fill_walls_with_water_or_fire(grid, width, height, water_prob, fire_prob):
    for y in range(height):
        for x in range(width):
            if isinstance(grid[y][x], Wall):
                rand_val = random.random()
                if rand_val < water_prob:
                    grid[y][x] = Water((x, y))  # Replace Wall with Water
                elif rand_val < water_prob + fire_prob:
                    grid[y][x] = Fire((x, y))  # Replace Wall with Fire



width, height = 100, 100
num_paths = 2  # Adjustable number of paths
spike_prob = 0.1  # 10% chance to place Spikes in empty spaces
water_prob = 0.05  # 5% chance for Water on walls
fire_prob = 0.05  # 5% chance for Fire on walls

def generateMap():
    return generate_path_level(width, height, num_paths, spike_prob, water_prob, fire_prob)


        
