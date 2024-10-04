import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position  # Tuple (x, y)
        self.parent = parent      # Reference to the parent Node

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return False  # For heapq operations, required for comparison

# Possible directions and their corresponding movement deltas (x, y)
DIRECTIONS = {
    0: (1, 0),    # Right
    90: (0, -1),  # Up
    180: (-1, 0), # Left
    270: (0, 1)   # Down
}


# Function that calculate The Manhattan Distance Heuristics (the estimated cost from current position to goal.)
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

# A* pathfinding function to find the shortest path from `start` to `goal`.
def a_star(start, goal, game_map):

    open_set = [] # A open set as a priority queue to explore nodes by their priority (lowest f_score first)
    start_node = Node(start)
    heapq.heappush(open_set, (0, start_node))  # Add the start position with an initial f_score of 0

    g_score = {start_node: 0} # cost of getting from the start to each position
    f_score = {start_node: heuristic(start, goal)} # estimated total cost from start to goal (g_score + heuristic)

    # while the open set is not empty
    while open_set:
        # Get the node with the lowest f_score from the priority queue
        current_node = heapq.heappop(open_set)[1]

        # If we have reached the goal, reconstruct the path
        if current_node.position == goal:
            return reconstruct_path_from_node(current_node)

        # Iterate through each possible direction (right, up, left, down)
        for direction, (dx, dy) in DIRECTIONS.items():
            # Calculate the neighbor position by adding direction deltas to the current position
            neighbor_position = (current_node.position[0] + dx, current_node.position[1] + dy)

            # Skip this neighbor if it's not a valid move (e.g., out of bounds, obstacle)
            if not is_valid_move(neighbor, game_map):
                continue

            # The cost to move to this neighbor is current cost (`g_score[current]`) + 1 (assuming each move has a cost of 1)
            tentative_g_score = g_score[current_node.position] + 1

            # If this neighbor is unvisited, add it to the open_set
            if neighbor not in g_score:
                neighbor_node = Node(neighbor_position, current_node)
                g_score[neighbor_position] = tentative_g_score
                f_score[neighbor_position] = tentative_g_score + heuristic(neighbor_position, goal)
                heapq.heappush(open_set, (f_score[neighbor_position], neighbor_node))

    # no path found
    return None

# Function to check if a move is valid (not out of bounds and no obstacle)
def is_valid_move(position, game_map):
    x, y = position
    # Check if the position is out of bounds of the map
    if x < 0 or y < 0 or x >= len(game_map) or y >= len(game_map[0]):
        return False
    # Check if there is an obstacle at this position
    tile = game_map[x][y]
    obstacle = tile.get('obstacle')
    if obstacle and obstacle.get('textureIndex') != 8:
        return False
    # If all checks pass, the move is valid
    return True

# Function to reconstruct the path from the end node
def reconstruct_path_from_node(current_node):
    path = []
    while current_node:
        path.append(current_node.position)
        current_node = current_node.parent  # Move to the parent node
    path.reverse()  # Reverse to get path from start to goal
    return path

# Function to get the direction for the next step in the path
def get_next_direction(entity_position, player_position, game_map):
    # Use A* to find the shortest path from the entity to the player
    path = a_star(entity_position, player_position, game_map)
    # If there's no path or the entity is already at the player, there's no move to make
    if not path or len(path) < 2:
        return None

    # The next step on the path towards the player
    next_step = path[1]
    dx = next_step[0] - entity_position[0]
    dy = next_step[1] - entity_position[1]

    # Find the corresponding direction from the delta values
    for direction, (dir_dx, dir_dy) in DIRECTIONS.items():
        if (dx, dy) == (dir_dx, dir_dy):
            return direction

    # If we can't determine the direction, return None (shouldn't happen with a valid path)
    return None

