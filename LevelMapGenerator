import random

class GameObject:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol 

# Rooms, Items, Hallways, Doors, Decorations, and Hazards are subclasses of GameObject
class Room(GameObject):
    def __init__(self):
        super().__init__('Room', 'R')

class Item(GameObject):
    def __init__(self, name):
        super().__init__(name, 'I')

class Hallway(GameObject):
    def __init__(self):
        super().__init__('Hallway', 'H')

class Door(GameObject):
    def __init__(self):
        super().__init__('Door', 'D')

class Decoration(GameObject):
    def __init__(self, name):
        super().__init__(name, 'X')

class Hazard(GameObject):
    def __init__(self, name, damage):
        super().__init__(name, 'H')
        self.damage = damage


# LevelMap class to represent and generate the map
class LevelMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.rooms = []
        self.hallways = []
        self.items = []
        self.doors = []
        self.decorations = []
        self.hazards = []

    def generate_room(self, x, y, w, h):
        for i in range(y, min(y + h, self.height)):
            for j in range(x, min(x + w, self.width)):
                self.grid[i][j] = 'R'
        self.rooms.append(Room())

    def generate_hallway(self, x1, y1, x2, y2):
        # Draw a hallway from (x1, y1) to (x2, y2)

        # Vertical hallway
        if x1 == x2:  
            for i in range(min(y1, y2), max(y1, y2) + 1):
                self.grid[i][x1] = 'H'

        # Horizontal hallway
        elif y1 == y2:  
            for j in range(min(x1, x2), max(x1, x2) + 1):
                self.grid[y1][j] = 'H'
        self.hallways.append(Hallway())

    def add_door(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 'D'
        self.doors.append(Door())

    def add_item(self, x, y, item_name):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 'I'
        self.items.append(Item(item_name))

    def add_decoration(self, x, y, decoration_name):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 'X'
        self.decorations.append(Decoration(decoration_name))

    def add_hazard(self, x, y, hazard_name, damage):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 'H'
        self.hazards.append(Hazard(hazard_name, damage))

    def display_map(self):
        for row in self.grid:
            print(' '.join(row))

# Basic random generated level
def generate_level():
    level = LevelMap(20, 10)

    # Generate rooms and hallways
    # Room at (2,2) with width 5 and height 3
    level.generate_room(2, 2, 5, 3)  

    # Room at (12,5) with width 6 and height 4
    level.generate_room(12, 5, 6, 4) 

    # Hallway connecting the rooms
    level.generate_hallway(7, 3, 12, 3)  

    # Add doors
    level.add_door(7, 3) 

    # Add items, decorations, and hazards
    level.add_item(3, 3, "Health Potion")
    level.add_decoration(13, 6, "Statue") 
    level.add_hazard(10, 4, "Fire", 10) 

    level.display_map()


generate_level()
