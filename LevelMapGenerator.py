import random

# Constants for level grid size and room dimensions
GRID_WIDTH = 150
GRID_HEIGHT = 150
MIN_ROOM_SIZE = 10
MAX_ROOM_SIZE = 30
NUM_ROOMS = 8 

class Room:
    def __init__(self, x, y, width, height):
        self.x = x  # Top-left x coordinate
        self.y = y  # Top-left y coordinate
        self.width = width
        self.height = height

    # Check if this room intersects with another room
    def intersects(self, other):
        return not (self.x + self.width <= other.x or 
                    other.x + other.width <= self.x or
                    self.y + self.height <= other.y or 
                    other.y + other.height <= self.y)


    # Randomly pick an edge (left, right, top, bottom) and return a position on that edge
    def random_edge_position(self):
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            door_x, door_y = random.randint(self.x, self.x + self.width - 1), self.y - 1  
            hallway_start_x, hallway_start_y = door_x, self.y - 2
        elif edge == 'bottom':
            door_x, door_y = random.randint(self.x, self.x + self.width - 1), self.y + self.height  
            hallway_start_x, hallway_start_y = door_x, self.y + self.height + 1
        elif edge == 'left':
            door_x, door_y = self.x - 1, random.randint(self.y, self.y + self.height - 1)  
            hallway_start_x, hallway_start_y = self.x - 2, door_y
        elif edge == 'right':
            door_x, door_y = self.x + self.width, random.randint(self.y, self.y + self.height - 1)  
            hallway_start_x, hallway_start_y = self.x + self.width + 1, door_y
        
        return (door_x, door_y), (hallway_start_x, hallway_start_y)

class Level:
    def __init__(self, width, height, num_rooms):
        self.width = width
        self.height = height
        self.num_rooms = num_rooms
        self.rooms = []
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]

    
    # Randomly place non-overlapping rooms
    def generate_rooms(self):
        for _ in range(self.num_rooms):
            while True:
                width = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
                height = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
                x = random.randint(0, self.width - width - 1)
                y = random.randint(0, self.height - height - 1)
                
                new_room = Room(x, y, width, height)

                # check new room doesn't overlap with existing rooms
                if all(not new_room.intersects(other_room) for other_room in self.rooms):
                    self.rooms.append(new_room)
                    break

    # Prim's algorithm to connect all rooms in a minimal spanning tree
    def connect_rooms(self):
        connected_rooms = [self.rooms[0]]
        unconnected_rooms = self.rooms[1:]
        hallways = []

        while unconnected_rooms:
            room_a = random.choice(connected_rooms)
            room_b = random.choice(unconnected_rooms)

            # Connect rooms via hallways through door tiles
            hallway = self.create_hallway(room_a, room_b)
            hallways.append(hallway)
            connected_rooms.append(room_b)
            unconnected_rooms.remove(room_b)
        
        return hallways

    def create_hallway(self, room1, room2):
        # Get door positions and hallway starting points for both rooms
        (door1_x, door1_y), (start1_x, start1_y) = room1.random_edge_position()
        (door2_x, door2_y), (start2_x, start2_y) = room2.random_edge_position()

        # Place doors on the grid
        self.grid[door1_y][door1_x] = 'D'
        self.grid[door2_y][door2_x] = 'D'

        # Create a hallway (L-shaped, first horizontal then vertical)
        hallway = []
        if random.choice([True, False]):
            # Horizontal first
            hallway.extend([(x, start1_y) for x in range(min(start1_x, start2_x), max(start1_x, start2_x) + 1)])
            hallway.extend([(start2_x, y) for y in range(min(start1_y, start2_y), max(start1_y, start2_y) + 1)])
        else:
            # Vertical first
            hallway.extend([(start1_x, y) for y in range(min(start1_y, start2_y), max(start1_y, start2_y) + 1)])
            hallway.extend([(x, start2_y) for x in range(min(start1_x, start2_x), max(start1_x, start2_x) + 1)])

        return hallway

    def place_rooms_and_hallways_on_grid(self, hallways):
        for room in self.rooms:
            for i in range(room.y, room.y + room.height):
                for j in range(room.x, room.x + room.width):
                    self.grid[i][j] = 'R'
        for hallway in hallways:
            for x, y in hallway:
                self.grid[y][x] = 'H'

    def display_grid(self):
        # Print the grid
        for row in self.grid:
            print(''.join(row))

# Generate the level
def generate_level():
    # Define the level parameters
    level = Level(GRID_WIDTH, GRID_HEIGHT, NUM_ROOMS)

    # Generate rooms randomly
    level.generate_rooms()  

    # Connect rooms with hallways
    hallways = level.connect_rooms()  

    # Place on grid
    level.place_rooms_and_hallways_on_grid(hallways) 

    # Step 4: Display level grid
    level.display_grid()  


generate_level()
