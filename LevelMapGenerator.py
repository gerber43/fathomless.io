import random

MIN_ROOM_SIZE = 10
MAX_ROOM_SIZE = 30
NUM_ROOMS = 8  

class Room:
    def __init__(self, room_id, x, y, width, height):
        self.room_id = room_id
        self.x = x  # Top-left x coordinate
        self.y = y  # Top-left y coordinate
        self.width = width
        self.height = height
        self.doors = []  # List of door keys (which door connects to which hallway)
        self.door_positions = set()  # Track positions where doors are placed

    def random_edge_position(self):
        # Randomly pick an edge (left, right, top, bottom) and return a door position on that edge
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            pos = (random.randint(self.x, self.x + self.width - 1), self.y - 1)
        elif edge == 'bottom':
            pos = (random.randint(self.x, self.x + self.width - 1), self.y + self.height)
        elif edge == 'left':
            pos = (self.x - 1, random.randint(self.y, self.y + self.height - 1))
        elif edge == 'right':
            pos = (self.x + self.width, random.randint(self.y, self.y + self.height - 1))

        return pos, edge

    def add_door(self, door_key, pos):
        # Ensure there are no overlapping doors in the same position
        if pos not in self.door_positions:
            self.door_positions.add(pos)
            self.doors.append(door_key)
            return True
        return False

class Hallway:
    def __init__(self, door_key_1, door_key_2, direction1, direction2):
        self.door_key_1 = door_key_1  # Connection to the first room's door
        self.door_key_2 = door_key_2  # Connection to the second room's door
        self.direction1 = direction1  # Direction from the first room
        self.direction2 = direction2  # Direction to the second room

    def __repr__(self):
        return f"Hallway between {self.door_key_1} and {self.door_key_2} (directions: {self.direction1} -> {self.direction2})"

class Level:
    def __init__(self, num_rooms):
        self.num_rooms = num_rooms
        self.rooms = []
        self.hallways = []
        self.room_path = []  # List to store the path between rooms

    def generate_rooms(self):
        # Randomly create rooms with no overlap
        for room_id in range(1, self.num_rooms + 1):
            while True:
                width = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
                height = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
                x = random.randint(0, 100 - width)  # For simplicity, assume a large enough area
                y = random.randint(0, 100 - height)
                
                new_room = Room(room_id, x, y, width, height)

                # Ensure the new room doesn't overlap with existing rooms
                if all(not self.overlaps(new_room, other_room) for other_room in self.rooms):
                    self.rooms.append(new_room)
                    break

    def overlaps(self, room1, room2):
        return not (room1.x + room1.width <= room2.x or
                    room2.x + room2.width <= room1.x or
                    room1.y + room1.height <= room2.y or
                    room2.y + room2.height <= room1.y)

    def connect_rooms(self):
        # Prim's algorithm to create a connected graph (MST)
        connected_rooms = [self.rooms[0]]
        unconnected_rooms = self.rooms[1:]

        while unconnected_rooms:
            room_a = random.choice(connected_rooms)
            room_b = random.choice(unconnected_rooms)

            # Get door positions and directions
            (door1_pos, direction1) = room_a.random_edge_position()
            (door2_pos, direction2) = room_b.random_edge_position()

            # Generate door keys based on room_id and direction
            door_key_1 = f"Room{room_a.room_id}_Door{direction1}_{door1_pos}"
            door_key_2 = f"Room{room_b.room_id}_Door{direction2}_{door2_pos}"

            # Only connect if there are no overlapping doors in the same position
            if room_a.add_door(door_key_1, door1_pos) and room_b.add_door(door_key_2, door2_pos):
                # Create a hallway between the two doors
                hallway = Hallway(door_key_1, door_key_2, direction1, direction2)

                # Add the hallway
                self.hallways.append(hallway)

                # Add the connection between rooms to the path
                self.room_path.append((room_a.room_id, room_b.room_id))

                connected_rooms.append(room_b)
                unconnected_rooms.remove(room_b)

    def generate_level(self):
        self.generate_rooms()
        self.connect_rooms()
        level_layout = {
            "rooms": [(room.room_id, room.doors) for room in self.rooms],
            "hallways": [str(hallway) for hallway in self.hallways],
            "path_between_rooms": self.room_path  #(room_a_id, room_b_id)
        }
        return level_layout




def generate_level():
    level = Level(NUM_ROOMS)
    return level.generate_level()

# Output generated level
level_layout = generate_level()
print(level_layout)
